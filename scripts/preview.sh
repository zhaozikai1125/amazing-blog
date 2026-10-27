#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
python3 scripts/build.py
printf '\n博客已在本机预览： http://127.0.0.1:8765/\n按 Ctrl+C 停止预览。\n\n'
exec python3 -m http.server 8765 --bind 127.0.0.1 --directory site
