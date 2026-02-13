import json

from langchain_core.messages.base import messages_to_dict

from app.agent import ReactGraph
from app.db import init_db, insert_conversation, update_messages_snapshot

NAME_MAX_LEN = 50


def call_agent(user_input: str, model: str, host: str):
    # get user input from console
    audit = ReactGraph(model=model, host=host)
    result = audit.run(user_input)
    # print result
    print(result)

    # Add messages to database using existing db functions
    init_db()
    state = result.get("messages") or {}
    messages = state.get("messages") or []
    if messages:
        prompt = user_input  # we already have it from input
        response = (result.get("response") or "").strip()
        name = (
            (prompt[:NAME_MAX_LEN] + "...")
            if len(prompt) > NAME_MAX_LEN
            else (prompt or "Untitled")
        )
        permit_id = insert_conversation(name=name, prompt=prompt, response=response)
        messages_dict = messages_to_dict(list(messages))
        update_messages_snapshot(permit_id, json.dumps(messages_dict, default=str))
        print(f"Saved to database (conversation id={permit_id})")
