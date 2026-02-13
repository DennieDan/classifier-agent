"""Seed the permits table with conversation data from process_format.py. Run from project root: python seed_conversation.py."""

import json
import os
import sys

# Ensure project root and app are on path
_ROOT = os.path.dirname(os.path.abspath(__file__))
_APP = os.path.join(_ROOT, "app")
sys.path.insert(0, _ROOT)
sys.path.insert(0, _APP)
os.chdir(_APP)

from db import init_db, insert_conversation, update_messages_snapshot, update_response
from langchain_core.messages.base import messages_to_dict

from process_format import data


def main() -> None:
    init_db()
    messages = data["messages"]
    if not messages:
        print("No messages in process_format.data")
        return
    # First human message as prompt
    prompt = ""
    for m in messages:
        if type(m).__name__ == "HumanMessage":
            prompt = getattr(m, "content", "") or ""
            break
    name = (
        prompt[:50] + ("..." if len(prompt) > 50 else "")
        if prompt
        else "Virgin Olive Oil (sample)"
    )
    final_content = ""
    for m in reversed(messages):
        content = getattr(m, "content", "") or ""
        if content and "final".lower() or "Final" in content.lower():
            final_content = content
            break
    permit_id = insert_conversation(
        name=name,
        prompt=prompt or "What is the HS-Code of Virgin Olive Oil?",
        response=final_content,
    )
    messages_dict = messages_to_dict(messages)
    update_messages_snapshot(permit_id, json.dumps(messages_dict, default=str))
    if final_content:
        update_response(permit_id, final_content)
    print(f"Inserted permit id={permit_id}, name={name!r}")


if __name__ == "__main__":
    main()
