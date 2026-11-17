# Phase 1 - Linux, Git, Networking and Python (Days 1-12)

**Goal:** be comfortable in a Linux terminal, write reliable bash and Python scripts,
and use Git daily. Everything later (Docker, Kubernetes, Terraform, CI/CD) assumes this.

**Daily rhythm (about 4 hours):** 1.5 h learn, 2 h hands-on lab, 30 min notes and a Git commit.
If you only learn by reading you will forget it. If a lab is not finished, finish it before moving on.

**Where to practise Linux:** WSL2 on Windows, a free Ubuntu VM (Azure free tier B1s or
AWS free tier t3.micro), or Multipass/VirtualBox. Use Ubuntu 22.04 or 24.04.

---

## Day-by-day plan

### Day 1 - Linux filesystem and navigation
- **Learn:** filesystem hierarchy (`/etc`, `/var`, `/home`, `/proc`, `/opt`), absolute vs relative paths.
- **Do:** `ls -la`, `cd`, `pwd`, `cp`, `mv`, `rm`, `mkdir -p`, `touch`, `cat`, `less`, `head`, `tail -f`, `find`, `which`, `man`.
- **Lab:** build a project tree with one command, find all `.log` files modified today, view a log live with `tail -f`.
- **Done when:** you can move around without a GUI and explain what lives in `/etc` and `/var/log`.

### Day 2 - Users, groups and permissions
- **Learn:** users, groups, `sudo`, file modes (`rwx`, octal `755`), ownership, umask, setuid basics.
- **Do:** `useradd`, `usermod -aG`, `passwd`, `chmod`, `chown`, `id`, `whoami`, `visudo`.
- **Lab:** create user `deploy`, a shared folder only the `devs` group can write to, then prove it with `su`.
- **Done when:** you can read `-rwxr-x---` instantly and fix a "Permission denied" error.

### Day 3 - Processes and services (systemd)
- **Learn:** processes, signals, foreground/background, `systemd` units and targets, `journalctl`.
- **Do:** `ps aux`, `top`/`htop`, `kill`, `pkill`, `nice`, `systemctl status|start|stop|enable`, `journalctl -u <svc> -f`.
- **Lab:** install `nginx`, enable it, break its config on purpose, find the error in `journalctl`, fix it. Then write your own tiny systemd service that runs `labs/python/system_report.py` every minute using a timer.
- **Done when:** you can answer "service X is down, what do you do?" with a method, not guesses.

### Day 4 - Packages, networking and troubleshooting
- **Learn:** `apt` (and `dnf`), IP addressing, DNS, ports, TCP vs UDP, HTTP status codes, TLS basics, firewalls.
- **Do:** `apt update/install`, `ip a`, `ip route`, `ping`, `traceroute`, `dig`, `nslookup`, `curl -v`, `ss -tlnp`, `nc -zv`, `ufw`.
- **Lab:** for `https://example.com` capture each stage: DNS lookup (`dig`), TCP connect (`nc -zv host 443`), TLS and HTTP (`curl -v`). Write down what a failure at each stage looks like.
- **Done when:** you can narrow "the site is down" to DNS, network, TLS or application.
- **AVD link:** this is the same layered thinking you used for AVD connectivity tickets.

### Day 5 - Bash scripting 1 (text processing)
- **Learn:** pipes, redirection (`>`, `>>`, `2>&1`), `grep`, `awk`, `sed`, `sort`, `uniq`, `cut`, `wc`.
- **Lab:** read `labs/bash/log_filter.sh`, run it on `labs/data/access.log`, then extend it to show the IP address with the most 4xx responses.
- **Done when:** you can answer questions about a log file with one-line pipelines.

### Day 6 - Bash scripting 2 (real scripts) and cron
- **Learn:** variables, arguments, `if`, loops, functions, exit codes, `set -euo pipefail`, `trap`, cron syntax.
- **Lab:** study `labs/bash/disk_alert.sh` and `labs/bash/backup.sh`. Schedule the backup in cron every 5 minutes, verify retention works by faking old files with `touch -d`.
- **Stretch:** run `shellcheck` on every script and fix warnings.
- **Done when:** your scripts fail loudly and safely instead of silently.

### Day 7 - Git and GitHub workflow (+ week 1 review)
- **Learn:** commits, branches, merge vs rebase, `.gitignore`, pull requests, resolving conflicts, conventional commit messages.
- **Do:** `git init/clone/add/commit/branch/switch/merge/rebase/stash/log --oneline --graph/reset/revert`.
- **Lab:** create a branch, make conflicting changes on two branches, resolve the conflict, open a PR on GitHub, squash-merge it.
- **Review:** redo any Day 1-6 lab you found hard. Write a one-page cheat sheet in `notes/`.
- **Done when:** you never fear a merge conflict and use PRs even on your own repos.

### Day 8 - Python basics
- **Learn:** types, lists, dicts, sets, loops, functions, f-strings, virtual environments (`python3 -m venv`), `pip`.
- **Lab:** read `labs/python/system_report.py`, then add a field for the 5 largest files in `/var/log`.
- **Done when:** you can write a 30-line script from a blank file.

### Day 9 - Python: files, JSON, regex, errors
- **Learn:** reading/writing files, `json`, `re`, exceptions (`try/except`), `with`, `pathlib`.
- **Lab:** read `labs/python/log_analyzer.py` line by line. Change the regex so it also captures the user agent. Add a `--status` filter flag.
- **Done when:** you can explain every line of `log_analyzer.py`.

### Day 10 - Python: command-line tools and HTTP
- **Learn:** `argparse`, `sys.exit`, `urllib`/`requests`, threads vs processes, timeouts.
- **Lab:** read and run `labs/python/health_checker.py` against 5 real URLs, including one that returns 500 and one that does not exist. Add a `--retries` option.
- **Done when:** your tool returns a meaningful exit code that a CI job could use.

### Day 11 - Python: testing, linting, logging
- **Learn:** `pytest`, fixtures, `flake8`, the `logging` module, small functions that are easy to test.
- **Lab:** run `pytest`, then write 3 new tests for features you added on Days 9-10. Replace `print` in one script with `logging`.
- **Done when:** `pytest` and `flake8` are green and you understand why the tests are structured this way.

### Day 12 - Capstone: Ops toolkit
Build one polished tool, `opskit`, that combines what you learned. Suggested features:
1. `opskit disk` - disk usage report with a threshold and non-zero exit when exceeded.
2. `opskit logs <file>` - access log analysis from `log_analyzer.py`.
3. `opskit check <urls...>` - health checks from `health_checker.py`.
4. Tests for each command, a README with usage examples, and the CI workflow green.

**Done when:** a stranger can clone the repo, run three commands from your README, and it works.

---

## Cheat sheets

### Linux troubleshooting method
1. What changed? (deploy, config, certificate, disk, traffic)
2. Is the process running? `systemctl status`, `ps`
3. What do the logs say? `journalctl -u svc -n 100`, `/var/log/*`
4. Resources: `df -h`, `free -h`, `top`
5. Network: `ss -tlnp`, `curl -v`, `dig`
6. Narrow down, change one thing at a time, write down what you tried

### Must-know one-liners
```bash
find /var/log -type f -name "*.log" -mtime -1          # logs changed in last day
du -sh /var/* 2>/dev/null | sort -h | tail             # biggest folders
grep -ri "error" /var/log/syslog | tail -20            # recent errors
ss -tlnp | grep :80                                    # who owns port 80
ps aux --sort=-%mem | head                             # memory hogs
journalctl -u nginx --since "10 min ago"               # recent service logs
```

## Check yourself (answer out loud)
1. What is the difference between a process and a service?
2. What does `chmod 640 file` allow, and for whom?
3. `2>&1` - what does it do?
4. How do you find which process is using port 8080?
5. What happens, in order, when you type a URL into a browser?
6. Why use `set -euo pipefail` in bash scripts?
7. `list` vs `tuple` vs `set` vs `dict` in Python - when do you use each?
8. How would you make a Python script safe to run from cron?
