#!/bin/bash
# MathTeacherPage 一键部署脚本
# Token 已安全存储在 macOS Keychain，无需明文

set -e
cd "$(dirname "$0")"

echo "=========================================="
echo "  MathTeacherPage 部署到 GitHub Pages"
echo "=========================================="
echo ""

# 提交所有更改
git add -A
git commit -m "更新: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || echo "无更改需提交"

# 推送（从 Keychain 读取 token）
git push origin main

echo ""
echo "✓ 部署完成！"
echo "  访问地址：https://tsing-cv.github.io/MathTeacherPage/"
echo ""
