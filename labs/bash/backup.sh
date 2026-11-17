#!/usr/bin/env bash
# backup.sh - timestamped tar.gz backup with retention.
# Day 6 lab. Concepts: tar, date, find -mtime, trap, safe scripting.
#
# Usage: ./backup.sh <source_dir> <backup_dir> [keep_days]
set -euo pipefail

SRC="${1:?usage: backup.sh <source_dir> <backup_dir> [keep_days]}"
DEST="${2:?usage: backup.sh <source_dir> <backup_dir> [keep_days]}"
KEEP_DAYS="${3:-7}"

[[ -d "$SRC" ]] || { echo "source not found: $SRC" >&2; exit 1; }
mkdir -p "$DEST"

STAMP="$(date +%Y%m%d-%H%M%S)"
ARCHIVE="$DEST/$(basename "$SRC")-$STAMP.tar.gz"
TMP="$ARCHIVE.partial"

# Remove the partial file if anything fails half way.
trap 'rm -f "$TMP"' ERR INT TERM

tar -czf "$TMP" -C "$(dirname "$SRC")" "$(basename "$SRC")"
mv "$TMP" "$ARCHIVE"
echo "created $ARCHIVE ($(du -h "$ARCHIVE" | cut -f1))"

# Delete backups older than KEEP_DAYS.
find "$DEST" -name "$(basename "$SRC")-*.tar.gz" -mtime +"$KEEP_DAYS" -print -delete
