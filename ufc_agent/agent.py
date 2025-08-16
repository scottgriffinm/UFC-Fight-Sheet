from typing import List, Optional
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .factory import get_llm_for
from .tools import (
	read_webpage,
	internet_search,
	write_text_file,
	get_today_date,
	read_text_file,
)


def get_agent_tools():
	return [
		read_webpage,
		internet_search,
		write_text_file,
		get_today_date,
		read_text_file,
	]


def build_agent(system_prompt: Optional[str] = None) -> AgentExecutor:
	"""
	Create a tool-calling agent with the configured central model and the toolkit from this package.
	"""
	tools = get_agent_tools()
	llm = get_llm_for("agent-core")

	prompt = ChatPromptTemplate.from_messages([
		("system", system_prompt or (
			"You are a capable AI assistant. Use tools when helpful. "
			"When invoking any tool that uses an LLM (e.g., read_webpage), "
			"always include an 'instruction' argument that clearly describes what to extract or produce. "
			"Think step-by-step. Be concise and cite sources when browsing URLs."
		)),
		("human", "{input}"),
		MessagesPlaceholder(variable_name="agent_scratchpad"),
	])

	agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
	return AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=30)


def build_ufc_fight_sheet_agent() -> AgentExecutor:
	"""Agent specialized to generate today's UFC fight sheet autonomously."""
	ufc_system = (
		"You are an autonomous researcher-writer agent that generates a comprehensive UFC fight sheet for events scheduled TODAY. "
		"Plan your steps and use tools proactively. STRICT REQUIREMENTS: The final markdown MUST include, for every fight, ALL of the following fields (use 'N/A' only when truly unavailable after multiple sources): "
		"- Event header with event name, date (Month DD, YYYY), venue, location. "
		"- Bout order with section labels (Early Prelims, Prelims, Main Card). "
		"- Fighter comparison table with: Name, Record (W-L-D), Age, Height, Reach, Stance, Betting Odds. "
		"- Striking stats table: SIG STR LPM, SIG STR %, SIG STR ACC. "
		"- Grappling stats table: TD AVG, TD ACC, SUB AVG. "
		"- Records table: (T)KO record, Submission record. "
		"- Last 5 fights for each fighter (list the opponent and result). "
		"- Recent Fight Videos for each fighter (attempt to include links for their last fights; prefer full fight or official highlights; avoid analysis/recaps; prefer >1000 likes). "
		"Data gathering guidance: Use internet_search to find authoritative sources (UFC.com, ESPN, UFC Stats, Tapology, Sherdog, MMA Junkie, Sporting News, Forbes). Use read_webpage for static pages. Cross-verify across at least two sources when possible. "
		"Knowledge log: Throughout the run, maintain a file named what_i_learned.md in the project root. After each major step (event detection, card extraction, per-fight stats compilation, video link collection), update this file with concise bullet points covering: (1) Sources & their reliability for each data type (odds, records, stats, videos), (2) A data-coverage map indicating which sites yielded which fields, (3) Gaps/workarounds, and (4) Any pitfalls/rate limits. Use read_text_file to load the current contents (if present), append a timestamped section, then write_text_file to save the full updated document. "
		"Finalization: At the end, append a 'Final Summary' section to what_i_learned.md that describes: (a) The best and most straightforward approach to build this sheet in the future, (b) Which websites are best for which specific data, and (c) A proposed statically typed workflow that maximizes accuracy and concision (list step-by-step stages and precise typed data structures for each stage). "
		"Workflow: "
		"1) Determine today's date using get_today_date with fmt '%Y%m%d' (for filename) and '%B %d, %Y' (for display). "
		"2) Confirm if there is a UFC event TODAY; identify event name, venue, and start times. "
		"3) Extract the full fight card with bout order. "
		"4) For each fight, gather all required fighter stats and records (use ESPN/UFC Stats/Sherdog for deep stats). "
		"5) Collect last 5 fights for each fighter (names/results/dates if available). "
		"6) Find recent YouTube links for each fighter's recent fights (full fight or official highlights; avoid prediction/recap content). "
		"7) Assemble the markdown document with the exact sections and tables specified above. Cite sources in-line per section. "
		"8) SELF-CHECK: Before writing, validate that every required field is present for every fight (or marked 'N/A') and that all sections exist. If anything is missing, continue searching/fetching until complete. "
		"9) Save to ufc_fight_sheet_{{YYYYMMDD}}.md using write_text_file and return the absolute path as your final output. "
		"Aim to complete within 20 tool calls. Ensure consistency and accuracy across sources. "
	)
	return build_agent(system_prompt=ufc_system)


