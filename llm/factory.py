# llm/factory.py
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from llm.settings import LLM_CONFIG

load_dotenv()

def get_llm_for(task: str = "default", **overrides):
    """
    Get langchain chat model for a given task
    """
    # Grab the base task config
    task_cfg = LLM_CONFIG.get(task, LLM_CONFIG["default"]).copy()
    # Apply any runtime overrides
    task_cfg.update(overrides)

    # Get model name and temperature
    model_name = task_cfg["model_name"]
    
    # Lookup provider from the top-level available_models
    provider = (
        LLM_CONFIG
        .get("available_models", {})
        .get(model_name, {})
        .get("provider")
    )

    # Lookup temperature from the top-level available_models
    temperature = (
        LLM_CONFIG
        .get("available_models", {})
        .get(model_name, {})
        .get("temperature")
    )

    reasoning_effort = (
        LLM_CONFIG
        .get("available_models", {})
        .get(model_name, {})
        .get("reasoning_effort")
    )

    assert provider is not None, f"No provider configured for model '{model_name}'"

    # Initialize the model - most modern models have built-in web search
    if reasoning_effort:
        return init_chat_model(
            model_name,
            model_provider=provider,
            reasoning_effort=reasoning_effort,
            temperature=temperature,
            max_retries=3,
        )
    else:
        return init_chat_model(
            model_name, 
            model_provider=provider,
            temperature=temperature,
            max_retries=3,
        )