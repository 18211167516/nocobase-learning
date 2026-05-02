#!/bin/bash
echo "====================================="
echo "NocoBase 学习平台"
echo "====================================="
echo ""
echo "启动中..."
echo "访问地址: http://localhost:8000"
echo ""

cd "$(dirname "$0")"
python -m http.server 8000
