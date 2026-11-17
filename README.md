# 01 - Linux, Git, Networking and Python

Phase 1 of a 60-day journey from support engineer to DevOps engineer.
Start here: **[LEARNING.md](LEARNING.md)** has the day-by-day plan (Days 1-12).

## What is in this repo

```
LEARNING.md              day-by-day plan, cheat sheets, self-check questions
labs/bash/               sysreport.sh, disk_alert.sh, backup.sh, log_filter.sh
labs/python/             log_analyzer.py, health_checker.py, system_report.py
labs/data/access.log     sample web log to practise on
tests/                   pytest tests for the Python labs
.github/workflows/ci.yml flake8, pytest and shellcheck on every push
```

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q

./labs/bash/sysreport.sh
./labs/bash/log_filter.sh labs/data/access.log
python3 labs/python/log_analyzer.py labs/data/access.log --top 3
python3 labs/python/health_checker.py https://example.com
```

## Your deliverable for this phase

A Day 12 capstone called `opskit` (a small ops CLI) added to this repo, with tests and a
README. Keep committing every day: a green contribution graph is evidence of consistency.

Next phase: **02-docker-containers**.
