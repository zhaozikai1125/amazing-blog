#!/bin/bash
cd "$(dirname "$0")" || exit 1
./scripts/preview.sh
status=$?
if [ "$status" -ne 0 ] && [ "$status" -ne 130 ]; then
    echo
    echo "启动失败，错误代码：$status"
    read -r -p "按回车键关闭窗口……" _
fi
