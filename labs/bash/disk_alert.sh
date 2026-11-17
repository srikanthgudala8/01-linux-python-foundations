#!/usr/bin/env bash
# disk_alert.sh - exit non-zero if any filesystem is above a usage threshold.
# Day 6 lab. Concepts: arguments, defaults, loops, conditionals, exit codes, cron.
#
# Usage:  ./disk_alert.sh [threshold_percent]     (default 80)
# Cron :  */15 * * * * /path/to/disk_alert.sh 85 || logger -t disk_alert "disk usage high"
set -euo pipefail

THRESHOLD="${1:-80}"

if ! [[ "$THRESHOLD" =~ ^[0-9]+$ ]]; then
  echo "threshold must be a number, got: $THRESHOLD" >&2
  exit 2
fi

status=0
while read -r usage mount; do
  pct="${usage%\%}"
  if (( pct >= THRESHOLD )); then
    echo "ALERT: $mount is at ${pct}% (threshold ${THRESHOLD}%)"
    status=1
  fi
done < <(df -P -x tmpfs -x devtmpfs | awk 'NR>1 {print $5, $6}')

[[ $status -eq 0 ]] && echo "OK: all filesystems below ${THRESHOLD}%"
exit $status
