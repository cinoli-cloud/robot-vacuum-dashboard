# Robot Vacuum Competitive Intelligence Dashboard

智能扫地机器人品牌出海行业的GTM竞品价格监控系统

## 功能特性

✅ **实时价格监控**
- 监控Top8品牌的所有在售产品
- 支持多渠道价格对比（官网、Amazon、Walmart、Costco、eBay）
- 24小时价格变化追踪

✅ **数据可视化**
- 响应式HTML看板界面
- 价格趋势图表（过去30天）
- 价格预测（未来7天）
- 品牌平均价格对比

✅ **新闻追踪**
- 各品牌最新动态（每品牌5条）
- 自动聚合行业新闻

✅ **自动更新**
- 每天8:00 AM自动更新数据
- 支持手动触发更新

## 监控品牌（基于2026年真实产品线）

1. **iRobot** (Roomba) - 4个产品 - 已被Picea Robotics收购
2. **Roborock** - 6个产品 - CES 2026新品Saros 20 Sonic (35,000Pa)
3. **Ecovacs** (Deebot) - 5个产品 - CES 2026新品X12 Pro Omni
4. **Dreame** - 6个产品 - CES 2026新品X60超薄系列
5. **Shark** - 3个产品 - PowerDetect系列
6. **Eufy** (Anker子品牌) - 3个产品 - CES 2026新品Omni S2 (30,000Pa)
7. **Narwal** - 3个产品 - CES 2026新品Flow 2
8. **Dyson** - 1个产品 - 360 Vis Nav (最强吸力)

**总计：31个2026年在售产品** ✅

## 系统架构

```
robot-vacuum-dashboard/
├── index.html              # 主看板页面
├── css/
│   └── style.css          # 样式文件
├── js/
│   └── app.js             # 前端交互逻辑
├── data/
│   └── products.json      # 数据文件
├── python/
│   ├── config.py          # 配置文件
│   ├── price_scraper.py   # 价格爬虫
│   ├── news_scraper.py    # 新闻爬虫
│   ├── generate_demo_data.py  # 演示数据生成器
│   ├── update_dashboard.py    # 主更新脚本
│   ├── scheduler.py       # 自动调度系统
│   └── requirements.txt   # Python依赖
└── README.md              # 说明文档
```

## 快速开始

### 1. 安装依赖

```bash
cd python
pip install -r requirements.txt
```

### 2. 生成初始数据

```bash
python generate_demo_data.py
```

### 3. 本地预览

打开 `index.html` 文件即可查看看板。

### 4. 启动自动更新

```bash
# 方式1: 单次手动更新
python update_dashboard.py

# 方式2: 启动自动调度器（每天8:00更新）
python scheduler.py
```

## 部署方案

### 方案1: 静态网站托管

最简单的方案，适合快速部署：

```bash
# 使用内置的web-visualizer skill部署
# 系统会自动上传HTML/CSS/JS到云端并生成访问链接
```

### 方案2: 服务器部署

适合需要后端自动更新的场景：

1. 将整个项目上传到服务器
2. 配置定时任务（cron）每天8:00运行更新脚本
3. 使用Nginx/Apache提供Web服务

```bash
# Linux crontab示例
0 8 * * * cd /path/to/project/python && python update_dashboard.py
```

## 数据更新方式

### 自动更新（推荐）

```bash
python scheduler.py
```

系统会：
- 立即执行一次更新
- 每天8:00 AM自动更新
- 记录日志到 `data/scheduler.log`

### 手动更新

```bash
python update_dashboard.py
```

或者在网页上点击 "Manual Update" 按钮。

## 数据合规说明

本系统的数据采集遵循以下原则：

✅ 遵守 robots.txt 协议
✅ 添加合理的请求延迟
✅ 使用合适的 User-Agent
✅ 仅抓取公开可访问的数据
✅ 不存储用户隐私信息

⚠️ **重要提示**：在生产环境中使用前，请确保：
1. 获得目标网站的爬取许可
2. 遵守当地数据隐私法规（GDPR、CCPA等）
3. 考虑使用官方API而非爬虫

## 真实数据爬取

当前版本使用演示数据。要切换到真实数据爬取：

1. 修改 `update_dashboard.py`
2. 取消注释真实爬虫导入
3. 处理反爬虫机制（可能需要代理、验证码处理等）

```python
# 替换这行
from generate_demo_data import ...

# 为
from price_scraper import PriceScraper
from news_scraper import NewsScraper
```

## 技术栈

- **前端**: HTML5 + CSS3 + JavaScript + Bootstrap 5 + Chart.js
- **后端**: Python 3.8+
- **数据采集**: Requests + BeautifulSoup4
- **调度**: Schedule
- **数据存储**: JSON

## 性能优化建议

1. **缓存策略**: 为静态资源添加CDN
2. **数据压缩**: 启用gzip压缩
3. **图片优化**: 品牌logo使用WebP格式
4. **懒加载**: 新闻卡片使用懒加载
5. **分批加载**: 大量产品时分页展示

## 常见问题

### Q: 数据多久更新一次？
A: 默认每天早上8:00自动更新，也可手动触发。

### Q: 支持哪些渠道？
A: 官网、Amazon、Walmart、Costco、eBay。可在config.py中添加更多渠道。

### Q: 如何添加新品牌？
A: 编辑 `python/config.py` 中的 `BRANDS_CONFIG`，添加品牌信息和产品列表。

### Q: 爬虫被封禁怎么办？
A:
1. 增加请求延迟
2. 使用代理IP池
3. 考虑使用官方API
4. 使用Selenium处理动态内容

### Q: 如何导出数据？
A: 数据保存在 `data/products.json`，可直接下载或导入到Excel/数据库。

## 未来改进

- [ ] 添加邮件/Slack通知（价格大幅变动时）
- [ ] 支持更多渠道（Target、Best Buy等）
- [ ] 添加用户认证系统
- [ ] 数据导出功能（Excel、CSV）
- [ ] 移动端App
- [ ] 价格警报功能
- [ ] 竞品对比分析报告生成

## 许可证

MIT License

## 联系方式

如有问题或建议，请联系项目维护者。

---

**最后更新**: 2026-01-12
**版本**: 1.0.0
