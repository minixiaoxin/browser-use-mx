# Browser-Use 中文使用指南

> 本项目是 Browser-Use 的源代码仓库，已升级到最新版本并添加了中文使用指南

## 📦 项目状态

✅ **已完成升级**
- Browser-Use SDK: v2.0.13
- Anthropic: v0.76.0
- OpenAI: v2.15.0
- Google GenAI: v1.60.0
- MCP: v1.26.0
- 所有依赖包已更新到最新版本

✅ **已配置 API Keys**
- BROWSER_USE_API_KEY ✓
- OPENROUTER_API_KEY ✓

---

## 🚀 快速开始

### 1. 最简单的方式（推荐新手）

```bash
# 执行预设的百度搜索任务
uv run python run_tasks.py tests/agent_tasks/baidu_search.yaml
```

### 2. 运行示例脚本

```bash
# 入门示例：百度搜索
uv run python my_first_automation.py

# 高级示例：批量查询GitHub仓库
uv run python advanced_automation.py

# 原有示例：查询GitHub星标
uv run python examples/simple.py
```

### 3. 交互式执行器

```bash
uv run python run_tasks.py
# 然后按提示选择要执行的任务
```

---

## 📚 文档导航

### 🎓 学习资源
- **[快速开始.md](快速开始.md)** - 5分钟快速上手指南
- **[如何创建自动化任务.md](如何创建自动化任务.md)** - 完整的任务创建教程

### 📝 示例文件

#### YAML任务文件（位于 `tests/agent_tasks/`）
- `baidu_search.yaml` - 百度搜索示例
- `github_stars.yaml` - GitHub星标查询
- `amazon_laptop.yaml` - Amazon商品搜索
- `browser_use_pip.yaml` - pip命令查询

#### Python脚本
- `my_first_automation.py` - 入门级示例
- `advanced_automation.py` - 高级示例（重试、批量、自定义工具）
- `run_tasks.py` - 任务执行器

---

## 🎯 三种创建任务的方式

### 方式 1️⃣：YAML 文件（最简单）

**创建** `tests/agent_tasks/my_task.yaml`：
```yaml
name: 我的任务
task: 在百度搜索"Python教程"，返回前3个结果
judge_context:
  - 必须访问百度
  - 必须搜索"Python教程"
  - 必须返回3个结果
max_steps: 10
```

**执行：**
```bash
uv run python run_tasks.py tests/agent_tasks/my_task.yaml
```

---

### 方式 2️⃣：Python 脚本（最灵活）

**创建** `my_script.py`：
```python
from browser_use import Agent, ChatBrowserUse
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    agent = Agent(
        task='在百度搜索"Python教程"，返回前3个结果',
        llm=ChatBrowserUse(),
    )
    
    history = await agent.run(max_steps=10)
    print(f"结果：{history.final_result()}")

if __name__ == "__main__":
    asyncio.run(main())
```

**执行：**
```bash
uv run python my_script.py
```

---

### 方式 3️⃣：同步方式（最快速）

**创建** `simple.py`：
```python
from browser_use import Agent, ChatBrowserUse
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    task='在百度搜索"Python教程"',
    llm=ChatBrowserUse(),
)

history = agent.run_sync()  # 同步执行
print(f"结果：{history.final_result()}")
```

**执行：**
```bash
uv run python simple.py
```

---

## 🔧 常用配置

### 显示/隐藏浏览器窗口（无头模式）

```python
from browser_use import Browser

# 显示窗口（开发调试推荐）
browser = Browser(
    headless=False,  # 可以看到浏览器操作过程
    window_size={'width': 1920, 'height': 1080},
)

# 隐藏窗口（生产环境推荐）
browser = Browser(
    headless=True,  # 后台运行，性能更好
)
```

**详细说明：** 查看 [无头模式详解.md](无头模式详解.md)

### 使用云端浏览器（绕过验证码）

```python
browser = Browser(
    use_cloud=True,  # 使用云端浏览器
    cloud_proxy_country_code='us',  # 使用美国代理
)
```

---

## 🔐 处理登录和授权

### 问题：每次运行都需要重新登录？

Browser-Use 每次运行都会创建新的浏览器实例，没有登录状态。以下是解决方案：

### 方案1：使用真实浏览器配置（推荐本地开发）

```python
from browser_use import Browser
import os

# 使用你已登录的 Chrome 浏览器配置
browser = Browser(
    # Windows
    executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    user_data_dir=os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data'),
    
    # macOS（取消注释）
    # executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    # user_data_dir=os.path.expanduser('~/Library/Application Support/Google/Chrome'),
    
    profile_directory='Default',
    headless=False,
)
```

**注意：** 使用前必须完全关闭 Chrome 浏览器！

### 方案2：保存和加载 Cookie（推荐生产环境）

```python
# 首次登录并保存
browser = Browser(
    user_data_dir='./browser_data',  # 保存到本地
    headless=False,
)

# 后续使用保存的状态
browser = Browser(
    user_data_dir='./browser_data',  # 使用保存的数据
    headless=True,
)
```

### 方案3：使用云端浏览器配置（最简单）

```bash
# 1. 创建云端配置（会打开浏览器让你登录）
export BROWSER_USE_API_KEY=your_key
curl -fsSL https://browser-use.com/profile.sh | sh
# 会返回一个 profile_id
```

```python
# 2. 使用云端配置
browser = Browser(
    use_cloud=True,
    cloud_profile_id='your-profile-id',  # 你的配置ID
)
```

**详细说明：** 查看 [登录授权解决方案.md](登录授权解决方案.md)

**快速开始：**
```bash
# 使用真实浏览器
uv run python use_real_browser.py

# 保存和加载Cookie
uv run python save_and_load_cookies.py
```

### 添加自定义工具

```python
from browser_use import Tools, ActionResult

tools = Tools()

@tools.action('保存到文件')
def save_file(content: str, filename: str) -> ActionResult:
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return ActionResult(
        extracted_content=f"已保存到 {filename}",
        success=True
    )

agent = Agent(
    task='你的任务',
    llm=ChatBrowserUse(),
    tools=tools,
)
```

---

## 📊 实用示例

### 示例 1：百度搜索

```python
from browser_use import Agent, ChatBrowserUse
import asyncio

async def search_baidu(keyword):
    agent = Agent(
        task=f'在百度搜索"{keyword}"，返回前5个结果的标题和链接',
        llm=ChatBrowserUse(),
    )
    history = await agent.run(max_steps=10)
    return history.final_result()

# 执行
result = asyncio.run(search_baidu("Python教程"))
print(result)
```

### 示例 2：GitHub 仓库信息

```python
from browser_use import Agent, ChatBrowserUse
import asyncio

async def get_github_info(repo):
    agent = Agent(
        task=f'''
        访问GitHub，搜索"{repo}"仓库
        返回：星标数、Fork数、主要语言
        ''',
        llm=ChatBrowserUse(),
    )
    history = await agent.run(max_steps=10)
    return history.final_result()

# 执行
result = asyncio.run(get_github_info("browser-use"))
print(result)
```

### 示例 3：批量任务

```python
from browser_use import Agent, ChatBrowserUse
import asyncio

async def batch_search(keywords):
    results = []
    for keyword in keywords:
        agent = Agent(
            task=f'在百度搜索"{keyword}"，返回第一个结果',
            llm=ChatBrowserUse(),
        )
        history = await agent.run(max_steps=8)
        results.append({
            'keyword': keyword,
            'result': history.final_result()
        })
    return results

# 执行
keywords = ["Python", "JavaScript", "Go"]
results = asyncio.run(batch_search(keywords))
for r in results:
    print(f"{r['keyword']}: {r['result']}")
```

---

## 🐛 常见问题

### 1. 浏览器无法启动

```bash
# 重新安装 Chromium
uvx browser-use install
```

### 2. API Key 未设置

检查 `.env` 文件：
```
BROWSER_USE_API_KEY=your_key_here
```

### 3. 任务超时

增加步骤数：
```python
history = await agent.run(max_steps=20)  # 增加到20步
```

### 4. 网站访问被拒绝

使用云端浏览器：
```python
browser = Browser(use_cloud=True)
```

---

## 📁 项目结构

```
browser-use-0.11.2/
├── 📚 中文文档
│   ├── README_CN.md                    # 本文件
│   ├── 快速开始.md                     # 快速上手指南
│   └── 如何创建自动化任务.md           # 完整教程
│
├── 🎯 任务文件
│   └── tests/agent_tasks/
│       ├── baidu_search.yaml           # 百度搜索
│       ├── github_stars.yaml           # GitHub查询
│       ├── amazon_laptop.yaml          # Amazon搜索
│       └── browser_use_pip.yaml        # pip命令查询
│
├── 🐍 示例脚本
│   ├── my_first_automation.py          # 入门示例
│   ├── advanced_automation.py          # 高级示例
│   ├── run_tasks.py                    # 任务执行器
│   └── examples/                       # 官方示例
│
├── 📦 核心代码
│   └── browser_use/                    # Browser-Use 源代码
│
└── 🔧 配置文件
    ├── .env                            # API Keys
    ├── pyproject.toml                  # 项目配置
    └── uv.lock                         # 依赖锁定
```

---

## 🌟 推荐学习路径

### 第1步：快速体验（5分钟）
```bash
uv run python run_tasks.py tests/agent_tasks/baidu_search.yaml
```

### 第2步：运行示例（10分钟）
```bash
uv run python my_first_automation.py
```

### 第3步：阅读文档（20分钟）
- 阅读 `快速开始.md`
- 阅读 `如何创建自动化任务.md`

### 第4步：创建自己的任务（30分钟）
- 创建 YAML 任务文件
- 或编写 Python 脚本

### 第5步：探索高级功能（1小时）
```bash
uv run python advanced_automation.py
```

---

## 🔗 相关链接

- **官方文档**: https://docs.browser-use.com
- **GitHub**: https://github.com/browser-use/browser-use
- **Discord社区**: https://link.browser-use.com/discord
- **云服务**: https://cloud.browser-use.com

---

## 💡 提示

1. **推荐使用 ChatBrowserUse 模型** - 专为浏览器自动化优化，速度快3-5倍
2. **遇到验证码？** - 使用 `Browser(use_cloud=True)` 云端浏览器
3. **需要代理？** - 设置 `cloud_proxy_country_code='us'`
4. **任务失败？** - 增加 `max_steps` 或优化任务描述

---

## 🎉 开始你的自动化之旅！

```bash
# 选择一个命令开始：

# 1. 最简单
uv run python run_tasks.py tests/agent_tasks/baidu_search.yaml

# 2. 入门示例
uv run python my_first_automation.py

# 3. 高级示例
uv run python advanced_automation.py

# 4. 交互模式
uv run python run_tasks.py
```

祝你使用愉快！🚀

---

**需要帮助？**
- 查看文档：`快速开始.md` 和 `如何创建自动化任务.md`
- 查看示例：`examples/` 目录
- 加入社区：https://link.browser-use.com/discord
