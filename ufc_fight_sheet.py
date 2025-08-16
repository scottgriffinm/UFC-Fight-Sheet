#!/usr/bin/env python
"""Create an info sheet on all the UFC fights scheduled for today using an autonomous agent."""

import argparse
import os, sys
from ufc_agent.agent import build_ufc_fight_sheet_agent


def main(limit: int | None = None):
    print("🚀 Starting UFC Fight Sheet Agent")
    agent = build_ufc_fight_sheet_agent()
    limit_hint = (
        f"Limit to the last {limit} fights in the event when generating the document. "
        if limit else ""
    )
    prompt = (
        "Generate today's UFC fight sheet end-to-end. "
        "Determine if there is a UFC event scheduled for today. If none, produce a short markdown stating no event and still save to file. "
        "If there is an event, gather all fights with the stats and recent YouTube links per requirements, assemble a well-formatted markdown document, "
        "and save it to a file named using today's date (e.g., ufc_fight_sheet_YYYYMMDD.md). "
        + limit_hint
    )
    result = agent.invoke({"input": prompt})
    print(result.get("output"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a UFC fight sheet for today using an autonomous agent.")
    parser.add_argument("--last-n-fights", type=int, default=None, help="Limit the number of fights to process (e.g., --last-n-fights 5).")
    args = parser.parse_args()
    main(args.last_n_fights)

