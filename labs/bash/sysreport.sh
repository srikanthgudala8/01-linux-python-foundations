#!/usr/bin/env bash
# sysreport.sh - print a quick health report for a Linux host.
# Day 5 lab. Concepts: variables, functions, command substitution, pipes, exit codes.
set -euo pipefail

section() { printf '\n== %s ==\n' "$1"; }

section "Host"
echo "Hostname : $(hostname)"
echo "Kernel   : $(uname -r)"
echo "Uptime   : $(uptime -p 2>/dev/null || uptime)"

section "CPU and memory"
echo "CPU cores: $(nproc)"
echo "Load avg : $(cut -d' ' -f1-3 /proc/loadavg)"
free -h | awk 'NR==1 || /^Mem:/'

section "Disk usage (top 5 by use%)"
df -hP -x tmpfs -x devtmpfs | awk 'NR==1 {print; next} {print | "sort -k5 -nr"}' | head -6

section "Top 5 processes by memory"
ps -eo pid,comm,%mem,%cpu --sort=-%mem | head -6

section "Listening TCP ports"
if command -v ss >/dev/null 2>&1; then
  ss -tln | awk 'NR>1 {print $4}' | sed 's/.*://' | sort -n | uniq | tr '\n' ' '
  echo
else
  echo "ss not installed"
fi
