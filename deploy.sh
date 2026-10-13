#!/bin/bash
# ========================================
# 一键部署脚本：MathTeacherPage → Surge.sh
# 首次运行需要输入邮箱（免费注册）
# ========================================

set -e

echo "=========================================="
echo "  MathTeacherPage 部署到 Surge.sh"
echo "=========================================="
echo ""

# 检查 surge 是否安装
if ! command -v surge &> /dev/null; then
  echo "正在安装 surge..."
  npm install -g surge
  echo "✓ surge 安装完成"
fi

echo ""
echo "首次使用需要登录（免费）："
echo "1. 输入你的邮箱（任意邮箱，用于接收 token）"
echo "2. 检查邮箱，复制 token 粘贴回来"
echo "3. 部署完成！"
echo ""
echo "按回车开始..."
read

# 进入项目目录
cd "$(dirname "$0")"

# 部署
echo ""
echo "正在部署..."
surge --project . --domain math-teacher-trng-cv.surge.sh

echo ""
echo "=========================================="
echo "  ✓ 部署完成！"
echo "=========================================="
echo ""
echo "稳定访问地址："
echo "  https://math-teacher-trng-cv.surge.sh"
echo ""
echo "请用这个 URL 更新二维码："
echo "  assets/qrcode-wechat.png"
echo ""
echo "以后更新网页后，重新运行此脚本即可："
echo "  ./deploy.sh"
echo ""
