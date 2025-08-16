from typing import Dict, Any
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .factory import get_llm_for
from .tools import read_text_file, read_webpage


JUDGE_SYSTEM = (
	"You are a strict QA judge for a UFC fight sheet. Your job is to read the produced markdown and judge whether it satisfies ALL required fields from the project README. "
	"Required per fight: bout order & section, fighter comparison (Name, Record W-L-D, Age, Height, Reach, Stance, Betting Odds), Striking (SIG STR LPM, SIG STR %, SIG STR ACC), Grappling (TD AVG, TD ACC, SUB AVG), Records ((T)KO, Submissions), Last 5 fights, Recent Fight Videos. Also require event header with event name, date (Month DD, YYYY), venue, location. Use 'N/A' only if truly unavailable. "
	"Return a strict JSON object with keys: verdict ('pass'|'fail'), missing_fields (list of strings), notes (string), and suggestions (list of strings)."
)


def build_judge_agent() -> AgentExecutor:
	llm = get_llm_for("agent-core")
	tools = [read_text_file, read_webpage]
	prompt = ChatPromptTemplate.from_messages([
		("system", JUDGE_SYSTEM),
		("human", "{input}"),
		MessagesPlaceholder(variable_name="agent_scratchpad"),
	])
	agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
	return AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)


def judge_file(markdown_path: str) -> Dict[str, Any]:
	agent = build_judge_agent()
	query = (
		"Load the specified markdown with read_text_file and evaluate against requirements. "
		f"Target file: {markdown_path}. "
		"Return JSON only."
	)
	result = agent.invoke({"input": query})
	# Try to parse content as JSON-like output
	output = result.get("output", "").strip()
	try:
		import json
		return json.loads(output)
	except Exception:
		return {"verdict": "fail", "missing_fields": [], "notes": output, "suggestions": ["Ensure judge returns valid JSON."]}
