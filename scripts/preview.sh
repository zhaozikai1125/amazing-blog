#!/bin/sh
set -eu
cd "$(dirname "$0")/.."

if ! command -v python3 >/dev/null 2>&1; then
    echo "没有找到 Python 3。请先安装 Python 3，再重新启动。"
    exit 1
fi

if [ ! -x .venv/bin/python ]; then
    echo "首次启动：正在创建项目专用 Python 环境……"
    python3 -m venv .venv
fi
PYTHON=.venv/bin/python

if ! "$PYTHON" -c 'import markdown' >/dev/null 2>&1; then
    echo "正在安装博客构建依赖……"
    "$PYTHON" -m pip install -r requirements.txt
fi

"$PYTHON" scripts/build.py
printf '\n博客已在本机预览： http://127.0.0.1:8765/\n浏览器打开上方地址。按 Ctrl+C 停止预览。\n\n'
exec "$PYTHON" -m http.server 8765 --bind 127.0.0.1 --directory site
