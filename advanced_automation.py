"""
高级浏览器自动化示例
功能：
1. 批量查询GitHub仓库信息
2. 使用自定义工具保存结果
3. 错误处理和重试机制
"""

from browser_use import Agent, Browser, Tools, ChatBrowserUse, ActionResult
from dotenv import load_dotenv
import asyncio
import json
from datetime import datetime

load_dotenv()


# 创建自定义工具
tools = Tools()


@tools.action('保存JSON数据到文件')
def save_json(data: str, filename: str) -> ActionResult:
    """
    保存数据到JSON文件
    
    Args:
        data: 要保存的数据（JSON字符串）
        filename: 文件名
    """
    try:
        # 尝试解析JSON
        json_data = json.loads(data) if isinstance(data, str) else data
        
        # 添加时间戳
        json_data['timestamp'] = datetime.now().isoformat()
        
        # 保存到文件
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        return ActionResult(
            extracted_content=f"✅ 数据已保存到 {filename}",
            success=True
        )
    except Exception as e:
        return ActionResult(
            extracted_content=f"❌ 保存失败：{str(e)}",
            error=str(e),
            success=False
        )


@tools.action('询问用户确认')
def ask_user(question: str) -> str:
    """
    在需要时询问用户
    
    Args:
        question: 要问的问题
    """
    print(f"\n❓ {question}")
    answer = input("👉 请输入 (yes/no): ").strip().lower()
    return f"用户回答：{answer}"


async def get_github_repo_info(repo_name: str, max_retries: int = 3):
    """
    获取GitHub仓库信息（带重试机制）
    
    Args:
        repo_name: 仓库名称（如 "browser-use/browser-use"）
        max_retries: 最大重试次数
    
    Returns:
        仓库信息字典
    """
    for attempt in range(max_retries):
        try:
            print(f"\n{'='*60}")
            print(f"📦 正在获取 {repo_name} 的信息... (尝试 {attempt + 1}/{max_retries})")
            print(f"{'='*60}")
            
            browser = Browser(
                headless=False,
                window_size={'width': 1920, 'height': 1080},
            )
            
            agent = Agent(
                task=f'''
                访问GitHub，找到 "{repo_name}" 仓库
                提取以下信息并以JSON格式返回：
                {{
                    "repo_name": "{repo_name}",
                    "stars": "星标数",
                    "forks": "Fork数",
                    "language": "主要编程语言",
                    "description": "仓库描述"
                }}
                ''',
                llm=ChatBrowserUse(),
                browser=browser,
                tools=tools,
            )
            
            history = await agent.run(max_steps=15)
            
            if history.is_done():
                result = history.final_result()
                print(f"\n✅ 成功获取信息！")
                print(f"结果：{result}")
                return {
                    'success': True,
                    'repo': repo_name,
                    'data': result,
                    'urls_visited': history.urls()
                }
            else:
                print(f"\n⚠️ 任务未完成，准备重试...")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)  # 等待2秒后重试
                    
        except Exception as e:
            print(f"\n❌ 发生错误：{str(e)}")
            if attempt < max_retries - 1:
                print(f"等待2秒后重试...")
                await asyncio.sleep(2)
            else:
                return {
                    'success': False,
                    'repo': repo_name,
                    'error': str(e)
                }
    
    return {
        'success': False,
        'repo': repo_name,
        'error': '达到最大重试次数'
    }


async def batch_query_repos(repo_list: list):
    """
    批量查询多个仓库信息
    
    Args:
        repo_list: 仓库名称列表
    """
    print(f"\n🚀 开始批量查询 {len(repo_list)} 个仓库...")
    
    results = []
    
    for repo in repo_list:
        result = await get_github_repo_info(repo)
        results.append(result)
        
        # 在查询之间稍作延迟，避免请求过快
        await asyncio.sleep(1)
    
    # 统计结果
    success_count = sum(1 for r in results if r['success'])
    fail_count = len(results) - success_count
    
    print(f"\n{'='*60}")
    print(f"📊 批量查询完成！")
    print(f"{'='*60}")
    print(f"✅ 成功：{success_count} 个")
    print(f"❌ 失败：{fail_count} 个")
    
    # 保存结果到文件
    output_file = f"github_repos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 结果已保存到：{output_file}")
    
    return results


async def interactive_search():
    """
    交互式搜索模式
    """
    print("\n🎯 交互式GitHub仓库查询")
    print("=" * 60)
    
    while True:
        repo = input("\n请输入仓库名称（如 'browser-use/browser-use'，输入 'quit' 退出）: ").strip()
        
        if repo.lower() == 'quit':
            print("\n👋 再见！")
            break
        
        if not repo:
            print("❌ 仓库名称不能为空！")
            continue
        
        result = await get_github_repo_info(repo)
        
        if result['success']:
            print(f"\n✨ 查询成功！")
        else:
            print(f"\n😞 查询失败：{result.get('error', '未知错误')}")


async def main():
    """主函数"""
    print("🌟 高级浏览器自动化示例")
    print("=" * 60)
    
    # 选择运行模式
    print("\n请选择运行模式：")
    print("1. 批量查询预设仓库")
    print("2. 交互式查询")
    print("3. 查询单个仓库")
    
    choice = input("\n请输入选项 (1/2/3): ").strip()
    
    if choice == '1':
        # 批量查询模式
        repos = [
            'browser-use/browser-use',
            'microsoft/playwright',
            'puppeteer/puppeteer',
        ]
        await batch_query_repos(repos)
        
    elif choice == '2':
        # 交互式模式
        await interactive_search()
        
    elif choice == '3':
        # 单个查询模式
        repo = input("请输入仓库名称（如 'browser-use/browser-use'）: ").strip()
        if repo:
            await get_github_repo_info(repo)
        else:
            print("❌ 仓库名称不能为空！")
    
    else:
        print("❌ 无效的选项！")


if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("\n✨ 程序执行完成！")
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断程序")
    except Exception as e:
        print(f"\n❌ 程序出错：{str(e)}")
