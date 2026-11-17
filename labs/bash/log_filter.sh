#!/usr/bin/env bash
# log_filter.sh - answer common questions about a web access log using grep/awk/sort/uniq.
# Day 5 lab. Concepts: text-processing pipelines, the bread and butter of Linux troubleshooting.
#
# Usage: ./log_filter.sh labs/data/access.log
set -euo pipefail

LOG="${1:?usage: log_filter.sh <access.log>}"

echo "== Requests per HTTP status =="
awk '{print $9}' "$LOG" | sort | uniq -c | sort -nr

echo
echo "== Top 5 client IPs =="
awk '{print $1}' "$LOG" | sort | uniq -c | sort -nr | head -5

echo
echo "== Top 5 requested paths =="
awk '{print $7}' "$LOG" | sort | uniq -c | sort -nr | head -5

echo
echo "== 5xx errors =="
awk '$9 ~ /^5/ {print $4, $7, $9}' "$LOG"
