#!/bin/bash

# Robot Vacuum Dashboard Quick Start Script

echo "================================================"
echo "   Robot Vacuum Dashboard - Quick Start"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装，请先安装 Python 3"
    exit 1
fi

echo "✓ Python 3 已安装"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 未安装，请先安装 pip3"
    exit 1
fi

echo "✓ pip3 已安装"
echo ""

# Install dependencies
echo "步骤 1/3: 安装Python依赖..."
cd python
pip3 install -r requirements.txt -q
if [ $? -eq 0 ]; then
    echo "✓ 依赖安装成功"
else
    echo "❌ 依赖安装失败"
    exit 1
fi
echo ""

# Generate initial data
echo "步骤 2/3: 生成初始数据..."
python3 generate_demo_data.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ 数据生成成功"
else
    echo "❌ 数据生成失败"
    exit 1
fi
echo ""

# Show menu
echo "步骤 3/3: 选择运行模式"
echo ""
echo "请选择:"
echo "  1) 查看价格分析报告"
echo "  2) 导出数据到 CSV"
echo "  3) 手动更新数据"
echo "  4) 启动自动调度器（每天8:00更新）"
echo "  5) 在浏览器中打开看板"
echo "  0) 退出"
echo ""
read -p "请输入选项 (0-5): " choice

case $choice in
    1)
        echo ""
        echo "正在生成分析报告..."
        python3 analyze_price_trends.py
        ;;
    2)
        echo ""
        python3 export_data.py
        ;;
    3)
        echo ""
        python3 update_dashboard.py
        ;;
    4)
        echo ""
        echo "启动调度器..."
        echo "按 Ctrl+C 停止"
        python3 scheduler.py
        ;;
    5)
        cd ..
        if [ -f "index.html" ]; then
            echo ""
            echo "正在打开看板..."
            # Try different browsers
            if command -v xdg-open &> /dev/null; then
                xdg-open index.html
            elif command -v open &> /dev/null; then
                open index.html
            elif command -v start &> /dev/null; then
                start index.html
            else
                echo "请手动打开 index.html 文件"
            fi
        else
            echo "❌ index.html 文件未找到"
        fi
        ;;
    0)
        echo ""
        echo "退出"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "================================================"
echo "           完成！"
echo "================================================"
