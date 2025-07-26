# llm/llm_tasks.py

# This version expects **image URLs** (e.g. S3 links) rather than local file paths.
# It constructs the LangChain message in the OpenAI-Vision compatible format:
# [{"type": "text", "text": "…"}, {"type": "image_url", "image_url": {"url": "https://…"}}]

from typing import List, Dict

from langchain.schema import HumanMessage, SystemMessage
from llm.factory import get_llm_for
from pydantic import BaseModel, Field

async def test_llm(
    task: str = "test-llm",
) -> str:

    print(f"🔍 [{task}] Building prompt for test LLM...")
    print(f"   🤖 Using model: {task}")

    class TestLLMSchema(BaseModel):
        test_result: str = Field(description="return todays date in the format YYYY-MM-DD")

    # Initialise the model and wrap it with structured output parsing
    print(f"   ⚙️  Initializing LLM with structured output...")
    llm = get_llm_for(task).with_structured_output(TestLLMSchema)

    # Base textual part of the user message
    content = [
        {
            "type": "text",
            "text": f"Return todays date in the format YYYY-MM-DD",
        }
    ]
    # Compose the full chat messages
    messages = [
        SystemMessage(
            content=(
                "You are an expert in checking for UFC events today. Given the current date, check if there's a UFC event today, and if so, return the event name. If there is no event today, return ''."
            )
        ),
        HumanMessage(content=f"Return todays date in the format YYYY-MM-DD"),
    ]

    # Invoke the LLM and return the structured output
    print(f"   📡 Invoking LLM for test...")
    result = await llm.ainvoke(messages)

    print(f"   ✅ LLM finished. Test result: {result.test_result}")
    return result.test_result

async def event_search(
    task: str = "event-search",
) -> str:

    print(f"🔍 [{task}] Building prompt for event checker...")
    print(f"   🤖 Using model: {task}")

    class EventCheckerSchema(BaseModel):
        event_name: str = Field(description="The name of the event")

    # Initialise the model and wrap it with structured output parsing
    print(f"   ⚙️  Initializing LLM with structured output...")
    llm = get_llm_for(task).with_structured_output(EventCheckerSchema)

    # Base textual part of the user message
    from datetime import datetime
    today = datetime.now().strftime("%B %d, %Y")
    content = [
        {
            "type": "text",
            "text": f"Search the web for UFC events happening on {today} (TODAY) and return the event name if there is one. Be very specific about checking for events happening today ({today}), not upcoming events. If no UFC event is happening on {today}, return empty string. Examples of event names: 'UFC 291', 'UFC ON ABC: WHITTAKER VS. DE RIDDER', 'UFC FIGHT NIGHT: LEWIS VS. TEIXEIRA'.",
        }
    ]
    # Compose the full chat messages
    messages = [
        SystemMessage(
            content=(
                f"You are an expert in checking for UFC events happening TODAY ({today}). Use web search to find current information about UFC events scheduled for TODAY ({today}), not upcoming events. Search for 'UFC events today', 'UFC schedule today', or 'UFC fight card today' to get the most up-to-date information. If there's a UFC event happening TODAY ({today}), return the exact event name. If there is no event happening TODAY ({today}), return ''."
            )
        ),
        HumanMessage(content=content),
    ]

    # Invoke the LLM and return the structured output
    print(f"   📡 Invoking LLM for event search...")
    result = await llm.ainvoke(messages)

    print(f"   ✅ LLM finished. Event search result: {result.event_name}")
    return result.event_name


async def fight_info_search(
    event_name: str,
    task: str = "info-search",
) -> List[Dict]:

    print(f"📊 [{task}] Building prompt for fight info search...")
    print(f"   🤖 Using model: {task}")
    print(f"   📅 Event: {event_name}")

    class FightInfoSchema(BaseModel):
        fights: List[Dict] = Field(description="List of fights with detailed fighter information. Each fight should have: fighter1 (with name and stats), fighter2 (with name and stats), weight_class, main_event (boolean), co_main_event (boolean)")

    # Initialise the model and wrap it with structured output parsing
    print(f"   ⚙️  Initializing LLM with structured output...")
    llm = get_llm_for(task).with_structured_output(FightInfoSchema)

    # Base textual part of the user message
    content = [
        {
            "type": "text",
            "text": f"Search the web for detailed information about all fights in the UFC event: {event_name}. For each fight, provide fighter stats including betting odds, height, weight, age, reach, stance, striking stats, takedown stats, records, and last 5 fights. Ensure each fighter has a 'name' field and all other fields are optional.",
        }
    ]
    # Compose the full chat messages
    messages = [
        SystemMessage(
            content=(
                "You are an expert UFC analyst. Use web search to find current and accurate information about UFC fights and fighters from reliable sources. Provide detailed information about UFC fights including all fighter statistics, records, and recent performance data. Return structured data for each fight with comprehensive fighter information. Each fighter MUST have a 'name' field, all other fields are optional."
            )
        ),
        HumanMessage(content=content),
    ]

    # Invoke the LLM and return the structured output
    print(f"   📡 Invoking LLM for fight info search...")
    result = await llm.ainvoke(messages)

    print(f"   ✅ LLM finished. Found {len(result.fights)} fights")
    return result.fights


async def video_link_search(
    fighter_name: str,
    task: str = "video-search",
) -> List[str]:

    print(f"🎥 [{task}] Building prompt for video link search for {fighter_name}...")
    print(f"   🤖 Using model: {task}")
    print(f"   👊 Fighter: {fighter_name}")

    class VideoLinksSchema(BaseModel):
        video_urls: List[str] = Field(description="List of YouTube video URLs for the fighter's recent fights")

    # Initialise the model and wrap it with structured output parsing
    print(f"   ⚙️  Initializing LLM with structured output...")
    llm = get_llm_for(task).with_structured_output(VideoLinksSchema)

    # Use the templated prompt format
    prompt_text = f"""Search the web for YouTube videos of {fighter_name}'s three most recent UFC fights. Find full fight videos that are freely available to watch and currently viewable. If full fight videos aren't available, find partial clips/shorts instead. Ensure these are not fight prediction analysis videos, fight recaps, or videos of the ufc video game. Ensure each video has more than 1,000 likes.

For each of the three fights, try to find at least three different videos.

Return only the YouTube URLs in a structured format."""

    # Base textual part of the user message
    content = [
        {
            "type": "text",
            "text": prompt_text,
        }
    ]
    # Compose the full chat messages
    messages = [
        SystemMessage(
            content=(
                "You are an expert at finding UFC fight videos on YouTube. Use web search to find high-quality, viewable fight videos that meet specific criteria. Return only valid YouTube URLs that are currently accessible and meet the specified requirements."
            )
        ),
        HumanMessage(content=content),
    ]

    # Invoke the LLM and return the structured output
    print(f"   📡 Invoking LLM for video search...")
    result = await llm.ainvoke(messages)

    print(f"   ✅ LLM finished. Found {len(result.video_urls)} videos for {fighter_name}")
    return result.video_urls

