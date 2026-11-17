#!/usr/bin/env python3
"""Analyse a web server access log (Common/Combined Log Format).

Day 9-12 lab. Concepts: file I/O, regular expressions, dictionaries, collections.Counter,
argparse, JSON output, functions that are easy to test.

Usage:
    python3 log_analyzer.py labs/data/access.log
    python3 log_analyzer.py labs/data/access.log --top 3 --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from typing import Iterable

LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+) [^"]*" '
    r"(?P<status>\d{3}) (?P<size>\d+|-)"
)


def parse_line(line: str) -> dict | None:
    """Return a dict of fields for one log line, or None if it does not match."""
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None
    entry = match.groupdict()
    entry["status"] = int(entry["status"])
    entry["size"] = 0 if entry["size"] == "-" else int(entry["size"])
    return entry


def analyse(lines: Iterable[str], top: int = 5) -> dict:
    """Summarise parsed log lines."""
    entries = []
    malformed = 0
    for line in lines:
        if not line.strip():
            continue
        entry = parse_line(line)
        if entry is None:
            malformed += 1
        else:
            entries.append(entry)

    total = len(entries)
    statuses = Counter(e["status"] for e in entries)
    server_errors = sum(count for status, count in statuses.items() if status >= 500)

    return {
        "total_requests": total,
        "malformed_lines": malformed,
        "status_counts": dict(sorted(statuses.items())),
        "error_rate_5xx": round(server_errors / total, 4) if total else 0.0,
        "top_ips": Counter(e["ip"] for e in entries).most_common(top),
        "top_paths": Counter(e["path"] for e in entries).most_common(top),
        "bytes_sent": sum(e["size"] for e in entries),
    }


def render_text(report: dict) -> str:
    lines = [
        f"Total requests : {report['total_requests']}",
        f"Malformed lines: {report['malformed_lines']}",
        f"5xx error rate : {report['error_rate_5xx']:.1%}",
        f"Bytes sent     : {report['bytes_sent']}",
        "Status codes   : "
        + ", ".join(f"{s}={c}" for s, c in report["status_counts"].items()),
        "Top IPs        :",
    ]
    lines += [f"  {ip:<15} {count}" for ip, count in report["top_ips"]]
    lines.append("Top paths      :")
    lines += [f"  {path:<20} {count}" for path, count in report["top_paths"]]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("logfile", help="path to the access log")
    parser.add_argument("--top", type=int, default=5, help="how many top items to show")
    parser.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = parser.parse_args(argv)

    try:
        with open(args.logfile, encoding="utf-8") as handle:
            report = analyse(handle, top=args.top)
    except OSError as exc:
        print(f"error: cannot read {args.logfile}: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2) if args.json else render_text(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
