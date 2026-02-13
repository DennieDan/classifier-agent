"""NiceGUI interface: sidebar conversation list, main input/process/conversation view."""

import json
import uuid

from constants import MODEL_PAIRS
from db import (
    delete_conversation,
    get_conversation,
    get_messages_snapshot,
    init_db,
    insert_conversation,
    list_conversations,
    update_messages_snapshot,
    update_name,
    update_response,
)
from message_components import render_message_cards
from nicegui import background_tasks, ui

# State
selected_id: int | None = None
current_permit_id: int | None = None  # New conversation being "processed" (placeholder)
in_progress_ids: set[int] = set()
main_content: ui.element | None = None
conversation_list_container: ui.element | None = None

NAME_MAX_LEN = 50


def _client_still_valid(element: ui.element | None) -> bool:
    """Return True if the element exists and its client connection is still active."""
    if element is None:
        return False
    try:
        _ = element.client
        return True
    except RuntimeError:
        return False


def _truncate_name(name: str) -> str:
    if len(name) <= NAME_MAX_LEN:
        return name
    return name[: NAME_MAX_LEN - 3] + "..."


def _refresh_sidebar() -> None:
    if conversation_list_container is None or not _client_still_valid(
        conversation_list_container
    ):
        return
    try:
        conversation_list_container.clear()
        with conversation_list_container:
            for permit_id, name in list_conversations():
                with ui.row().classes(
                    "w-full items-center gap-2 cursor-pointer hover:bg-gray-100 rounded p-2 group"
                ).on("click", lambda _, pid=permit_id: _on_select_conversation(pid)):
                    ui.label(_truncate_name(name)).classes("flex-1 truncate min-w-0")
                    ui.button(icon="delete").props("flat round dense").classes(
                        "opacity-0 group-hover:opacity-100 shrink-0"
                    ).on("click.stop", lambda pid=permit_id: _on_delete_clicked(pid))
            if not list_conversations():
                ui.label("No conversations yet").classes("text-gray-500 italic")
    except RuntimeError:
        pass


def _on_select_conversation(permit_id: int) -> None:
    global selected_id, current_permit_id
    selected_id = permit_id
    current_permit_id = None
    _show_conversation_view(permit_id)


# All unique model ids from MODEL_PAIRS (order preserved)
MODEL_OPTIONS = list(dict.fromkeys(m for _, m in MODEL_PAIRS))

# Map UI host label to agent ReactGraph host argument
HOST_TO_AGENT = {
    "Cloud Groq": "cloud groq",
    "Local": "local",
    "Cloud OpenAI": "cloud openai",
}


def _show_input_view() -> None:
    global selected_id, current_permit_id
    selected_id = None
    current_permit_id = None
    if main_content is None:
        return
    main_content.clear()
    with main_content:
        with ui.column().classes("w-full max-w-2xl gap-4"):
            ui.label("Enter your prompt and press Enter").classes(
                "text-lg text-gray-600"
            )
            with ui.row().classes("w-full gap-4 items-center"):
                host_select = (
                    ui.select(
                        options=["Cloud Groq", "Local", "Cloud OpenAI"],
                        value="Cloud Groq",
                        label="Host",
                    )
                    .classes("min-w-40")
                    .props("outlined dense")
                )
                model_select = (
                    ui.select(
                        options=MODEL_OPTIONS,
                        value=MODEL_OPTIONS[0] if MODEL_OPTIONS else None,
                        label="Model",
                    )
                    .classes("min-w-48")
                    .props("outlined dense")
                )

            with ui.card().classes("w-full p-3 bg-blue-50 border border-blue-200"):
                ui.label(
                    "Current Supporting Models — please only choose these combinations:"
                ).classes("text-sm font-medium text-gray-700")
                with ui.column().classes("w-full mt-2 gap-1"):
                    for host_label, model_id in MODEL_PAIRS:
                        ui.label(f"• {host_label}: {model_id}").classes(
                            "text-sm text-gray-600"
                        )
            inp = (
                ui.input(placeholder="Type here...").classes("w-full").props("outlined")
            )

            def _submit() -> None:
                text = inp.value or ""
                model = model_select.value or "llama-3.3-70b-versatile"
                host_label = host_select.value or "Cloud Groq"
                host = HOST_TO_AGENT.get(host_label, "cloud groq")
                _on_submit(text, model=model, host=host)

            inp.on("keydown.enter", lambda e: _submit())
            ui.button("Submit", on_click=_submit).props("unelevated")


def _messages_to_dict_list(messages) -> list:
    """Convert state['messages'] (list of BaseMessage or mixed) to list of dicts for rendering."""
    from langchain_core.messages.base import messages_to_dict

    # LangGraph add_messages may yield list of BaseMessage
    return messages_to_dict(list(messages))


async def _run_agent_background(
    permit_id: int, user_input: str, model: str, host: str
) -> None:
    """Run the agent to completion in the background; save result to DB when done."""
    from agent import ReactGraph

    in_progress_ids.add(permit_id)
    try:
        react = ReactGraph(model=model, host=host)
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        state = await react.graph.ainvoke(
            {"messages": ("user", user_input)},
            config=config,
        )
        messages = state.get("messages") or []
        final_content = (messages[-1].content or "") if messages else ""
        update_response(permit_id, final_content)
        try:
            messages_dict = _messages_to_dict_list(messages)
            update_messages_snapshot(permit_id, json.dumps(messages_dict, default=str))
        except Exception:
            pass
    except Exception as e:
        update_response(permit_id, str(e))
    finally:
        in_progress_ids.discard(permit_id)
        if _client_still_valid(main_content) and selected_id == permit_id:
            try:
                _show_conversation_view(permit_id)
                _refresh_sidebar()
            except RuntimeError:
                pass


def _on_rename(permit_id: int, current_name: str) -> None:
    with ui.dialog() as dialog, ui.card().classes("min-w-80"):
        ui.label("Rename conversation")
        inp = ui.input(value=current_name).classes("w-full").props("outlined")
        with ui.row().classes("w-full justify-end gap-2 mt-4"):
            ui.button("Cancel", on_click=dialog.close)
            ui.button(
                "Save", on_click=lambda: _do_rename(permit_id, inp.value or "", dialog)
            )

    def _do_rename(pid: int, new_name: str, d: ui.dialog) -> None:
        d.close()
        if new_name.strip():
            update_name(pid, new_name.strip())
            _refresh_sidebar()
            if selected_id == pid:
                _show_conversation_view(pid)

    dialog.open()


def _on_delete_clicked(permit_id: int) -> None:
    """Open confirmation dialog; on confirm, delete conversation and refresh."""
    with ui.dialog() as dialog, ui.card().classes("min-w-80"):
        ui.label("Delete this conversation? This cannot be undone.").classes(
            "text-body"
        )
        with ui.row().classes("w-full justify-end gap-2 mt-4"):
            ui.button("Cancel", on_click=dialog.close)
            ui.button(
                "Delete",
                on_click=lambda: _do_delete(permit_id, dialog),
            ).props("color=negative unelevated")

    def _do_delete(pid: int, d: ui.dialog) -> None:
        global selected_id
        d.close()
        delete_conversation(pid)
        if selected_id == pid:
            selected_id = None
            _show_input_view()
        _refresh_sidebar()

    dialog.open()


def _show_conversation_view(permit_id: int) -> None:
    row = get_conversation(permit_id)
    if main_content is None or row is None:
        return
    _, name, prompt, response = row
    if permit_id in in_progress_ids:
        main_content.clear()
        with main_content:
            with ui.column().classes("w-full max-w-2xl gap-4"):
                with ui.row().classes("w-full items-center gap-2"):
                    ui.label(name).classes("text-lg font-medium flex-1")
                    ui.button(
                        icon="edit", on_click=lambda: _on_rename(permit_id, name)
                    ).props("flat round").tooltip("Rename")
                ui.label("Prompt").classes("font-medium text-gray-600")
                ui.label(prompt).classes("w-full rounded border p-4 bg-gray-50")
                ui.label("In progress").classes("font-medium text-gray-600 mt-2")
                ui.spinner(size="lg")
        return
    snapshot = get_messages_snapshot(permit_id)
    main_content.clear()
    with main_content:
        with ui.column().classes("w-full max-w-2xl gap-4"):
            with ui.row().classes("w-full items-center gap-2"):
                ui.label(name).classes("text-lg font-medium flex-1")
                ui.button(
                    icon="edit", on_click=lambda: _on_rename(permit_id, name)
                ).props("flat round").tooltip("Rename")
            if snapshot:
                try:
                    messages_dict = json.loads(snapshot)
                    cards_container = ui.column().classes("w-full gap-4")
                    render_message_cards(cards_container, messages_dict)
                except Exception:
                    ui.label("Prompt").classes("font-medium text-gray-600")
                    ui.label(prompt).classes("w-full rounded border p-4 bg-gray-50")
                    ui.label("Response").classes("font-medium text-gray-600 mt-2")
                    ui.label(response or "(No response yet)").classes(
                        "w-full rounded border p-4 bg-white"
                    )
            else:
                ui.label("Prompt").classes("font-medium text-gray-600")
                ui.label(prompt).classes("w-full rounded border p-4 bg-gray-50")
                ui.label("Response").classes("font-medium text-gray-600 mt-2")
                ui.label(response or "(No response yet)").classes(
                    "w-full rounded border p-4 bg-white"
                )


def _on_submit(
    text: str,
    model: str = "llama-3.3-70b-versatile",
    host: str = "cloud groq",
) -> None:
    global current_permit_id, selected_id
    if not text.strip():
        return
    selected_id = None
    name = (
        _truncate_name(text.strip())
        if len(text.strip()) > NAME_MAX_LEN
        else text.strip()
    )
    permit_id = insert_conversation(name=name, prompt=text.strip(), response="")
    current_permit_id = permit_id
    in_progress_ids.add(permit_id)
    background_tasks.create(_run_agent_background(permit_id, text.strip(), model=model, host=host))
    selected_id = permit_id
    _refresh_sidebar()
    _show_conversation_view(permit_id)


def _on_new_conversation() -> None:
    _show_input_view()


def _build_ui() -> None:
    global main_content, conversation_list_container
    with ui.row().classes("w-full h-screen"):
        # Left sidebar: conversation list
        with ui.column().classes("w-64 border-r bg-gray-50 p-4 gap-2 shrink-0"):
            ui.label("Conversations").classes("font-semibold text-lg")
            conversation_list_container = ui.column().classes(
                "w-full gap-1 overflow-auto"
            )
            _refresh_sidebar()

        # Main area: header + content
        with ui.column().classes("flex-1 flex flex-col min-w-0"):
            with ui.row().classes(
                "w-full items-center justify-end p-4 border-b bg-white"
            ):
                ui.space()
                ui.button(icon="add", on_click=_on_new_conversation).props(
                    "round flat"
                ).tooltip("New conversation")
            main_content = ui.column().classes("flex-1 overflow-auto p-6")
            _show_input_view()


def run_ui(port: int = 8080, title: str = "Classifier Agent") -> None:
    init_db()
    _build_ui()
    ui.run(port=port, title=title, reload=False)


if __name__ == "__main__":
    run_ui()
