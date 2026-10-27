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
URL=http://127.0.0.1:8765/

if "$PYTHON" -c 'from urllib.request import urlopen; urlopen("http://127.0.0.1:8765/", timeout=1).read(1)' >/dev/null 2>&1; then
    echo "预览服务已经运行，将打开 $URL"
else
    "$PYTHON" -m http.server 8765 --bind 127.0.0.1 --directory site &
    SERVER_PID=$!
    trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT INT TERM
    sleep 1
    echo "博客预览已启动：$URL"
    echo "保持此窗口打开；关闭预览时按 Ctrl+C。"
fi

if command -v open >/dev/null 2>&1; then
    open "$URL"
else
    echo "请在浏览器中打开：$URL"
fi

if [ "${SERVER_PID:-}" ]; then
    wait "$SERVER_PID"
fi
