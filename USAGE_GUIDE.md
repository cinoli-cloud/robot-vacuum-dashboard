# Robot Vacuum Dashboard 使用指南

完整的使用说明和最佳实践指南。

## 目录

1. [快速开始](#快速开始)
2. [日常使用](#日常使用)
3. [高级功能](#高级功能)
4. [数据分析](#数据分析)
5. [故障排除](#故障排除)

---

## 快速开始

### 一键启动（推荐）

```bash
chmod +x quickstart.sh
./quickstart.sh
```

这将自动完成：
- 检查Python环境
- 安装依赖
- 生成初始数据
- 提供交互式菜单

### 手动启动

#### 1. 安装依赖

```bash
cd python
pip install -r requirements.txt
```

#### 2. 生成初始数据

```bash
python generate_demo_data.py
```

#### 3. 查看看板

在浏览器中打开 `index.html` 或访问部署的在线链接。

---

## 日常使用

### 查看价格看板

**在线访问**：
- 打开部署链接查看实时数据

**本地查看**：
```bash
# macOS
open index.html

# Linux
xdg-open index.html

# Windows
start index.html
```

### 手动更新数据

```bash
cd python
python update_dashboard.py
```

更新完成后刷新浏览器即可看到最新数据。

### 启动自动更新

```bash
cd python
python scheduler.py
```

系统将：
- 立即执行一次数据更新
- 每天早上8:00自动更新
- 持续运行直到手动停止（Ctrl+C）

**生产环境部署**：

在Linux服务器上使用systemd或cron：

```bash
# 添加到crontab
0 8 * * * cd /path/to/project/python && python update_dashboard.py
```

---

## 高级功能

### 1. 价格趋势分析

生成详细的价格分析报告：

```bash
cd python
python analyze_price_trends.py
```

报告包含：
- ✓ 品牌价格竞争力分析
- ✓ 渠道价格对比
- ✓ 最优惠产品TOP10
- ✓ 显著价格变化

**示例输出**：
```
品牌价格竞争力分析
==================
iRobot:
  产品数量: 3
  平均价格: $877.05
  价格区间: $594.35 - $1194.73
  平均变化: +3.7%
  市场定位: 中高端市场 ⭐
```

### 2. 数据导出

导出数据到CSV格式用于进一步分析：

```bash
cd python
python export_data.py
```

生成文件：
- `data/price_export.csv` - 当前价格数据
- `data/price_history_export.csv` - 历史价格趋势
- `data/news_export.csv` - 新闻数据

**用途**：
- 在Excel中进行自定义分析
- 导入到数据库
- 生成自定义报告

### 3. 价格警报系统

监控价格变化并触发警报：

```bash
cd python
python price_alerts.py
```

**警报类型**：
- 📉 价格大幅下降（≥5%）
- 📈 价格大幅上涨（≥5%）
- 💰 价格低于阈值（默认$500）

**配置警报**：

编辑 `python/alert_config.json`：

```json
{
  "enabled": true,
  "rules": [
    {
      "name": "Large Price Drop",
      "type": "price_decrease",
      "threshold": -5.0,
      "enabled": true
    },
    {
      "name": "New Low Price",
      "type": "price_below",
      "threshold": 500,
      "enabled": true
    }
  ],
  "notification": {
    "email": {
      "enabled": false,
      "recipients": ["your-email@example.com"]
    },
    "slack": {
      "enabled": false,
      "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK"
    }
  }
}
```

---

## 数据分析

### 看板功能说明

#### 1. 价格对比表格

**功能**：
- 显示所有产品在各渠道的实时价格
- 按品牌筛选
- 显示24小时价格变化

**使用技巧**：
- 点击品牌按钮过滤特定品牌
- 查看"24h Change"列快速识别价格波动
- 绿色↓表示降价，红色↑表示涨价

#### 2. 价格趋势图表

**过去30天趋势**：
- 显示各品牌平均价格走势
- 鼠标悬停查看具体数值
- 识别价格周期性变化

**品牌对比图**：
- 柱状图对比各品牌平均价格
- 快速识别高端/中端/大众品牌

**7天价格预测**：
- 基于历史数据的价格趋势预测
- 虚线表示预测值
- 辅助采购决策

#### 3. 新闻追踪

**功能**：
- 各品牌最新动态
- 来源和发布时间
- 点击查看详情

**用途**：
- 了解品牌促销活动
- 跟踪新品发布
- 行业趋势分析

### 关键指标解读

**Total Products（总产品数）**：
- 当前监控的产品总数
- 标准值：23

**Price Changes（价格变化数）**：
- 24小时内价格发生变化的产品数
- 高值表示市场活跃

**Average Price（平均价格）**：
- 所有产品在所有渠道的平均价格
- 用于评估整体市场价格水平

---

## 故障排除

### 常见问题

#### Q1: 数据不更新

**检查**：
```bash
# 查看更新日志
cat data/update.log

# 手动触发更新
cd python
python update_dashboard.py
```

**可能原因**：
- 调度器未运行
- Python脚本出错
- 权限问题

#### Q2: 看板显示空白

**检查**：
```bash
# 确认数据文件存在
ls -lh data/products.json

# 查看浏览器控制台是否有JavaScript错误
# Chrome: F12 -> Console
```

**解决方案**：
- 重新生成数据：`python generate_demo_data.py`
- 清除浏览器缓存
- 检查文件权限

#### Q3: 图表不显示

**原因**：Chart.js加载失败

**解决方案**：
- 检查网络连接（需要加载CDN资源）
- 尝试使用本地Chart.js库
- 查看浏览器控制台错误信息

#### Q4: Python依赖安装失败

**检查Python版本**：
```bash
python --version
# 需要 Python 3.8+
```

**使用国内镜像**：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### Q5: 真实爬虫被封禁

**解决方案**：
1. **增加延迟**：
   ```python
   # config.py
   SCRAPER_CONFIG = {
       "request_delay": 5,  # 增加到5秒
   }
   ```

2. **使用代理**：
   ```python
   # 添加代理配置
   proxies = {
       'http': 'http://proxy-server:port',
       'https': 'https://proxy-server:port'
   }
   ```

3. **使用官方API**（推荐）：
   - Amazon Product Advertising API
   - Walmart Open API
   - 避免直接爬取

### 日志文件

**更新日志**：
```bash
tail -f data/update.log
```

**调度器日志**：
```bash
tail -f data/scheduler.log
```

---

## 性能优化

### 提升加载速度

1. **启用CDN**：
   - 使用CDN加速Bootstrap、Chart.js

2. **数据压缩**：
   ```bash
   # 压缩JSON文件
   gzip data/products.json
   ```

3. **图片优化**：
   - 品牌logo使用WebP格式
   - 启用懒加载

### 减少服务器负载

1. **缓存策略**：
   ```nginx
   # Nginx配置
   location ~* \.(css|js|jpg|png)$ {
       expires 7d;
   }
   ```

2. **分批更新**：
   - 将品牌分批更新，避免同时爬取
   - 减少被封禁风险

---

## 安全建议

### 数据隐私

1. **不记录用户信息**：
   - 仅收集公开价格数据
   - 不存储Cookie或Session

2. **遵守robots.txt**：
   - 尊重网站爬虫政策
   - 使用合理的请求频率

3. **合规性检查**：
   - GDPR合规（欧洲用户）
   - CCPA合规（加州用户）

### 访问控制

**添加认证**（可选）：

```html
<!-- index.html -->
<script>
// 简单的密码保护
const password = prompt("请输入访问密码：");
if (password !== "your-secure-password") {
    document.body.innerHTML = "访问被拒绝";
}
</script>
```

---

## 最佳实践

### 数据采集

1. **设置合理延迟**：2-5秒
2. **使用轮换User-Agent**
3. **添加错误重试机制**
4. **记录详细日志**

### 数据分析

1. **定期导出备份**
2. **对比多个时间点数据**
3. **关注价格波动异常**
4. **结合新闻分析价格变化原因**

### 团队协作

1. **共享在线链接**
2. **定期分享分析报告**
3. **设置Slack/邮件通知**
4. **建立价格决策流程**

---

## 扩展开发

### 添加新品牌

编辑 `python/config.py`：

```python
BRANDS_CONFIG = {
    "YourBrand": {
        "official_site": "https://yourbrand.com",
        "products": [
            {
                "name": "Product Name",
                "model": "Model-123",
                "amazon_search": "YourBrand Model-123",
                "walmart_search": "YourBrand Model-123",
            }
        ]
    }
}
```

### 添加新渠道

1. **更新配置**（`config.py`）
2. **实现爬虫方法**（`price_scraper.py`）
3. **更新前端显示**（`index.html`）

### API集成

替换爬虫为API调用：

```python
# price_scraper.py
def scrape_amazon_api(product_id):
    """使用Amazon Product Advertising API"""
    from amazon_paapi import AmazonAPI
    api = AmazonAPI(key, secret, tag, region)
    product = api.get_items(product_id)
    return product['price']
```

---

## 技术支持

### 获取帮助

- 📖 查看 README.md
- 🐛 检查日志文件
- 💬 联系项目维护者

### 贡献代码

欢迎提交Pull Request改进项目！

---

**最后更新**: 2026-01-12
**版本**: 1.0.0
