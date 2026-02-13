"""Render LangChain conversation messages as HUMAN / AI / TOOL cards."""

import json
from typing import Any

from nicegui import ui


def _copy_text(text: str) -> None:
    ui.run_javascript(f"navigator.clipboard.writeText({json.dumps(text)})")


def _render_human_card(data: dict) -> None:
    content = data.get("content") or ""
    with ui.card().classes("w-full rounded-lg border bg-gray-50"):
        with ui.row().classes("w-full items-center justify-between p-2 border-b"):
            ui.label("HUMAN").classes("font-semibold")
            ui.button(icon="content_copy", on_click=lambda: _copy_text(content)).props("flat round dense").tooltip(
                "Copy"
            )
        ui.label(content).classes("p-4 whitespace-pre-wrap")


def _render_ai_card(data: dict) -> None:
    content = (data.get("content") or "").strip()
    tool_calls = data.get("tool_calls") or []
    with ui.card().classes("w-full rounded-lg border bg-gray-50"):
        with ui.row().classes("w-full items-center justify-between p-2 border-b"):
            ui.label("AI").classes("font-semibold")
        if tool_calls:
            for tc in tool_calls:
                name = tc.get("name") or "tool"
                call_id = tc.get("id") or ""
                args = tc.get("args") or {}
                with ui.column().classes("w-full gap-2 p-4"):
                    with ui.row().classes("items-center gap-2"):
                        ui.label(name).classes("font-medium")
                        if call_id:
                            ui.label(call_id).classes("rounded-full bg-gray-200 px-2 py-0.5 text-xs")
                    if args:
                        with ui.column().classes("gap-1 font-mono text-sm"):
                            for k, v in args.items():
                                with ui.row().classes("gap-2"):
                                    ui.label(f"{k}:").classes("text-gray-600")
                                    ui.label(str(v) if not isinstance(v, (dict, list)) else json.dumps(v)).classes(
                                        "text-green-700"
                                    )
        if content:
            ui.label(content).classes("p-4 whitespace-pre-wrap")


def _render_tool_card(data: dict) -> None:
    content = data.get("content") or ""
    name = data.get("name") or "tool"
    tool_call_id = data.get("tool_call_id") or ""
    with ui.card().classes("w-full rounded-lg border bg-gray-50"):
        with ui.row().classes("w-full items-center justify-between p-2 border-b"):
            ui.label("TOOL").classes("font-semibold")
            ui.button(icon="content_copy", on_click=lambda: _copy_text(content)).props("flat round dense").tooltip(
                "Copy"
            )
        with ui.column().classes("w-full gap-2 p-4"):
            with ui.row().classes("items-center gap-2"):
                ui.label(name).classes("font-medium")
                if tool_call_id:
                    ui.label(tool_call_id).classes("rounded-full bg-gray-200 px-2 py-0.5 text-xs")
            ui.label(content).classes("whitespace-pre-wrap break-words text-sm")


def render_message_cards(container: ui.element, messages: list[dict]) -> None:
    """
    Render a list of message dicts (as from messages_to_dict) into HUMAN/AI/TOOL cards.
    Each item in messages should be {"type": "human"|"ai"|"tool", "data": {...}}.
    """
    container.clear()
    with container:
        for item in messages:
            msg_type = (item.get("type") or "").lower()
            data = item.get("data") or item
            if msg_type == "human":
                _render_human_card(data)
            elif msg_type == "ai":
                _render_ai_card(data)
            elif msg_type == "tool":
                _render_tool_card(data)
