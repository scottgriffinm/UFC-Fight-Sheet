from typing import Optional
import os
import httpx
from langchain.tools import tool
from langchain_tavily import TavilySearch

from .factory import get_llm_for


# Helpers
def _default_headers() -> dict:
	return {
		"User-Agent": (
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
			"(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
		),
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.9",
	}


def _jina_reader_url(url: str) -> str:
	# Transform any http/https url into Jina Reader endpoint
	stripped = url.split("://", 1)[-1]
	return f"https://r.jina.ai/http://{stripped}"


def _fetch_webpage_text_with_fallback(url: str, max_chars: int) -> tuple[str, str]:
	"""
	Try fetching the webpage HTML directly with robust headers.
	On failure (401/403/network), fall back to Jina Reader to get readable text.
	Returns (text, source), where source is "direct" or "jina".
	"""
	# First attempt: direct
	try:
		headers = _default_headers()
		with httpx.Client(headers=headers, timeout=20.0, follow_redirects=True) as client:
			r = client.get(url)
			r.raise_for_status()
			text = r.text[: max(0, max_chars)]
			if text.strip():
				return text, "direct"
	except Exception:
		pass

	# Fallback: Jina Reader
	try:
		jr_url = _jina_reader_url(url)
		with httpx.Client(timeout=20.0, follow_redirects=True) as client:
			r = client.get(jr_url)
			r.raise_for_status()
			text = r.text[: max(0, max_chars)]
			return text, "jina"
	except Exception:
		return "", "error"


@tool
def read_webpage(url: str, instruction: str, max_chars: int = 12000) -> str:
	"""
	Read a webpage and extract information per the provided instruction.
	"""
	webpage_text, source = _fetch_webpage_text_with_fallback(url, max_chars)
	if not webpage_text:
		return f"Failed to fetch webpage. URL: {url}"

	llm = get_llm_for("tool-read-webpage")
	messages = [
		{"role": "system", "content": "You are an expert web assistant. Follow the user's instruction precisely."},
		{"role": "user", "content": [{"type": "text", "text": f"Instruction:\n{instruction}\n\nSource: {source}\nURL: {url}\n\nWebpage contents:\n{webpage_text}"}]},
	]
	result = llm.invoke(messages)
	try:
		return result.content  # AIMessage
	except AttributeError:
		return str(result)


@tool
def internet_search(query: str, max_results: int = 5) -> str:
	"""
	Search the internet using Tavily and return top results with URLs and snippets.
	Requires TAVILY_API_KEY in the environment.
	"""
	search = TavilySearch(k=max_results)
	results = search.invoke(query)
	return results


@tool
def write_text_file(file_path: str, content: str, encoding: str = "utf-8") -> str:
	"""
	Write text content to a file on disk. Returns the absolute path written.
	"""
	abs_path = os.path.abspath(file_path)
	os.makedirs(os.path.dirname(abs_path) or ".", exist_ok=True)
	with open(abs_path, "w", encoding=encoding) as f:
		f.write(content)
	return f"WROTE: {abs_path}"


@tool
def get_today_date(fmt: str = "%Y%m%d") -> str:
	"""
	Return today's date formatted with the given strftime format (default YYYYMMDD).
	"""
	from datetime import datetime
	return datetime.now().strftime(fmt)


@tool
def read_text_file(file_path: str, max_chars: int = 500000) -> str:
	"""
	Read a local text file and return its contents (truncated to max_chars). Useful for judging outputs.
	"""
	abs_path = os.path.abspath(file_path)
	if not os.path.exists(abs_path):
		return f"File not found: {abs_path}"
	try:
		with open(abs_path, "r", encoding="utf-8") as f:
			data = f.read()
		return data[: max(0, max_chars)]
	except Exception as e:
		return f"Failed to read file {abs_path}: {e}"


