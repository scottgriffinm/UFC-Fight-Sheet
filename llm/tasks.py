# llm/llm_tasks.py

# This version expects **image URLs** (e.g. S3 links) rather than local file paths.
# It constructs the LangChain message in the OpenAI-Vision compatible format:
# [{"type": "text", "text": "…"}, {"type": "image_url", "image_url": {"url": "https://…"}}]

from typing import List, Tuple, Dict

from langchain.schema import HumanMessage, SystemMessage
from llm.factory import get_llm_for
from pydantic import BaseModel, Field

import asyncio



async def event_search(
    task: str = "event-search",
) -> str:

    print(
        f"[{task}] Building prompt for event checker..."
    )

    class EventCheckerSchema(BaseModel):
        event_name: str = Field(description="The name of the event")


    # Initialise the model and wrap it with structured output parsing
    llm = get_llm_for(task).with_structured_output(EventCheckerSchema)

    # Base textual part of the user message
    content = [
        {
            "type": "text",
            "text": f"Check if there's a UFC event today, and if so, return the event name",
        }
    ]
    # Compose the full chat messages
    messages = [
        SystemMessage(
            content=(
                "You are an expert in checking for UFC events today. Given the current date, check if there's a UFC event today, and if so, return the event name. If there is no event today, return ''."
            )
        ),
        HumanMessage(content=content),
    ]

    # Invoke the LLM and return the structured output
    print(f"[{task}] Invoking LLM …")
    result = await llm.ainvoke(messages)

    print(f"[{task}] LLM finished. Returning results.")
    return result.event_name

