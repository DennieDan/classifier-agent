"""NiceGUI interface: sidebar conversation list, main input/process/conversation view."""

import asyncio
from nicegui import ui

from db import (
    get_conversation,
    init_db,
    insert_conversation,
    list_conversations,
    update_name,
    update_response,
)

# State
selected_id: int | None = None
current_permit_id: int | None = None  # New conversation being "processed" (placeholder)
process_container: ui.element | None = None
main_content: ui.element | None = None
conversation_list_container: ui.element | None = None

NAME_MAX_LEN = 50


def _truncate_name(name: str) -> str:
    if len(name) <= NAME_MAX_LEN:
        return name
    return name[: NAME_MAX_LEN - 3] + "..."


def _refresh_sidebar() -> None:
    if conversation_list_container is None:
        return
    conversation_list_container.clear()
    with conversation_list_container:
        for permit_id, name in list_conversations():
            with ui.row().classes("w-full items-center gap-2 cursor-pointer hover:bg-gray-100 rounded p-2").on(
                "click", lambda _, pid=permit_id: _on_select_conversation(pid)
            ):
                ui.label(_truncate_name(name)).classes("flex-1 truncate")
        if not list_conversations():
            ui.label("No conversations yet").classes("text-gray-500 italic")


def _on_select_conversation(permit_id: int) -> None:
    global selected_id, current_permit_id
    selected_id = permit_id
    current_permit_id = None
    _show_conversation_view(permit_id)


def _show_input_view() -> None:
    global selected_id, current_permit_id
    selected_id = None
    current_permit_id = None
    if main_content is None:
        return
    main_content.clear()
    with main_content:
        with ui.column().classes("w-full max-w-2xl gap-4"):
            ui.label("Enter your prompt and press Enter").classes("text-lg text-gray-600")
            inp = ui.input(placeholder="Type here...").classes("w-full").props("outlined")
            inp.on("keydown.enter", lambda e: _on_submit(inp.value or ""))
            ui.button("Submit", on_click=lambda: _on_submit(inp.value or "")).props("unelevated")


def _show_process_view(permit_id: int, prompt: str) -> None:
    if main_content is None:
        return
    main_content.clear()
    with main_content:
        with ui.column().classes("w-full max-w-2xl gap-4"):
            ui.label("Process").classes("text-lg font-medium")
            with ui.column().classes("w-full gap-2 rounded border p-4 bg-gray-50"):
                # Placeholder process steps
                for msg in ["Thinking...", "Searching...", "Evaluating...", "Done."]:
                    ui.label(msg).classes("text-gray-700")
            placeholder_response = f"[Placeholder response for: {prompt[:80]}{'...' if len(prompt) > 80 else ''}]"
            ui.label("Response").classes("text-lg font-medium mt-4")
            ui.label(placeholder_response).classes("w-full rounded border p-4 bg-white")
            update_response(permit_id, placeholder_response)
            _refresh_sidebar()


def _on_rename(permit_id: int, current_name: str) -> None:
    with ui.dialog() as dialog, ui.card().classes("min-w-80"):
        ui.label("Rename conversation")
        inp = ui.input(value=current_name).classes("w-full").props("outlined")
        with ui.row().classes("w-full justify-end gap-2 mt-4"):
            ui.button("Cancel", on_click=dialog.close)
            ui.button("Save", on_click=lambda: _do_rename(permit_id, inp.value or "", dialog))

    def _do_rename(pid: int, new_name: str, d: ui.dialog) -> None:
        d.close()
        if new_name.strip():
            update_name(pid, new_name.strip())
            _refresh_sidebar()
            if selected_id == pid:
                _show_conversation_view(pid)

    dialog.open()


def _show_conversation_view(permit_id: int) -> None:
    row = get_conversation(permit_id)
    if main_content is None or row is None:
        return
    _, name, prompt, response = row
    main_content.clear()
    with main_content:
        with ui.column().classes("w-full max-w-2xl gap-4"):
            with ui.row().classes("w-full items-center gap-2"):
                ui.label(name).classes("text-lg font-medium flex-1")
                ui.button(icon="edit", on_click=lambda: _on_rename(permit_id, name)).props("flat round").tooltip(
                    "Rename"
                )
            ui.label("Prompt").classes("font-medium text-gray-600")
            ui.label(prompt).classes("w-full rounded border p-4 bg-gray-50")
            ui.label("Response").classes("font-medium text-gray-600 mt-2")
            ui.label(response or "(No response yet)").classes("w-full rounded border p-4 bg-white")


def _on_submit(text: str) -> None:
    global current_permit_id, selected_id
    if not text.strip():
        return
    selected_id = None
    name = _truncate_name(text.strip()) if len(text.strip()) > NAME_MAX_LEN else text.strip()
    permit_id = insert_conversation(name=name, prompt=text.strip(), response="")
    current_permit_id = permit_id
    selected_id = None
    _refresh_sidebar()
    _show_process_view(permit_id, text.strip())


def _on_new_conversation() -> None:
    _show_input_view()


def _build_ui() -> None:
    global main_content, conversation_list_container
    with ui.row().classes("w-full h-screen"):
        # Left sidebar: conversation list
        with ui.column().classes("w-64 border-r bg-gray-50 p-4 gap-2 shrink-0"):
            ui.label("Conversations").classes("font-semibold text-lg")
            conversation_list_container = ui.column().classes("w-full gap-1 overflow-auto")
            _refresh_sidebar()

        # Main area: header + content
        with ui.column().classes("flex-1 flex flex-col min-w-0"):
            with ui.row().classes("w-full items-center justify-end p-4 border-b bg-white"):
                ui.space()
                ui.button(icon="add", on_click=_on_new_conversation).props("round flat").tooltip("New conversation")
            main_content = ui.column().classes("flex-1 overflow-auto p-6")
            _show_input_view()


def run_ui(port: int = 8080, title: str = "Classifier Agent") -> None:
    init_db()
    _build_ui()
    ui.run(port=port, title=title, reload=False)


if __name__ == "__main__":
    run_ui()
