#!/usr/bin/env python3
"""Print a JSON system report using only the standard library.

Day 8-9 lab. Concepts: modules, platform/os/shutil, json, f-strings, reading /proc on Linux.
"""
from __future__ import annotations

import json
import os
import platform
import shutil


def memory_info() -> dict:
    """Parse /proc/meminfo (Linux only). Returns MiB values."""
    info = {}
    try:
        with open("/proc/meminfo", encoding="utf-8") as handle:
            for line in handle:
                key, value = line.split(":", 1)
                info[key] = int(value.split()[0]) // 1024
    except OSError:
        return {}
    return {"total_mib": info.get("MemTotal"), "available_mib": info.get("MemAvailable")}


def disk_info(path: str = "/") -> dict:
    usage = shutil.disk_usage(path)
    return {
        "path": path,
        "total_gib": round(usage.total / 2**30, 1),
        "used_percent": round(usage.used / usage.total * 100, 1),
    }


def build_report() -> dict:
    return {
        "hostname": platform.node(),
        "os": platform.platform(),
        "python": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "load_average": os.getloadavg() if hasattr(os, "getloadavg") else None,
        "memory": memory_info(),
        "disk": disk_info("/"),
    }


if __name__ == "__main__":
    print(json.dumps(build_report(), indent=2))
