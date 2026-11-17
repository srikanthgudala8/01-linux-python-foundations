#!/usr/bin/env python3
"""Check a list of URLs concurrently and report status and latency.

Day 10-12 lab. Concepts: HTTP from Python, threads (concurrent.futures), timeouts,
exceptions, exit codes so it can be used in CI or cron.

Usage:
    python3 health_checker.py https://example.com https://httpbin.org/status/500
    python3 health_checker.py --file urls.txt --timeout 3
Exit code is 0 if every URL is healthy, 1 otherwise.
"""
from __future__ import annotations

import argparse
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass


@dataclass
class Result:
    url: str
    ok: bool
    status: int | None
    latency_ms: float
    error: str = ""


def check(url: str, timeout: float = 5.0) -> Result:
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:  # noqa: S310
            status = resp.status
        error = ""
    except urllib.error.HTTPError as exc:  # server answered with 4xx/5xx
        status, error = exc.code, str(exc.reason)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        status, error = None, str(getattr(exc, "reason", exc))
    latency = (time.perf_counter() - start) * 1000
    return Result(url, status is not None and 200 <= status < 400, status, latency, error)


def check_all(urls: list[str], timeout: float = 5.0, workers: int = 8) -> list[Result]:
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(lambda u: check(u, timeout), urls))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("urls", nargs="*", help="URLs to check")
    parser.add_argument("--file", help="file with one URL per line")
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args(argv)

    urls = list(args.urls)
    if args.file:
        with open(args.file, encoding="utf-8") as handle:
            urls += [ln.strip() for ln in handle if ln.strip() and not ln.startswith("#")]
    if not urls:
        parser.error("provide at least one URL or --file")

    results = check_all(urls, args.timeout)
    for r in results:
        mark = "OK  " if r.ok else "FAIL"
        detail = r.status if r.status is not None else r.error
        print(f"{mark} {r.url:<45} {str(detail):<12} {r.latency_ms:7.1f} ms")
    return 0 if all(r.ok for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
