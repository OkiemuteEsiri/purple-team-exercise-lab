from __future__ import annotations

import argparse
from pathlib import Path

from outcome_evaluator import load_results
from reporting import render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate synthetic purple-team exercise results.")
    parser.add_argument("results", help="Path to synthetic JSON exercise results")
    parser.add_argument("--output", help="Optional Markdown report path")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    results = load_results(args.results)
    report = render_markdown(results)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
        print(f"Wrote {output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
