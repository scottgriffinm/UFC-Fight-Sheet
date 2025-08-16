#!/usr/bin/env python
import argparse
from ufc_agent.judge import judge_file

def main(path: str):
    verdict = judge_file(path)
    import json
    print(json.dumps(verdict, indent=2))

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Judge a UFC fight sheet markdown for completeness.")
    p.add_argument("path", help="Path to the generated markdown file")
    args = p.parse_args()
    main(args.path)
