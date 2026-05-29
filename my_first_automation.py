"""
我的第一个浏览器自动化脚本
功能：在百度搜索指定关键词，提取搜索结果
"""

from browser_use import Agent, Browser, ChatBrowserUse
from dotenv import load_dotenv
import asyncio

load_dotenv()


async def search_baidu(keyword: str):
    """
    在百度搜索关键词并提取结果
    
    Args:
        keyword: 要搜索的关键词
    
    Returns:
        搜索结果
    """
    print(f"\n🔍 开始搜索：{keyword}")
    print("=" * 50)
    
    # 创建浏览器配置（可选）
    browser = Browser(
        headless=False,  # 显示浏览器窗口，方便观察
        window_size={'width': 1920, 'height': 1080},
    )
    
    # 创建 Agent
    agent = Agent(
        task=f'''
        1. 访问百度搜索 (baidu.com)
        2. 搜索关键词："{keyword}"
        3. 提取前5个搜索结果的标题和链接
        4. 以清晰的格式返回结果
        ''',
        llm=ChatBrowserUse(),
        browser=browser,
    )
    
    # 执行任务
    history = await agent.run(max_steps=10)
    
    # 处理结果
    if history.is_done():
        print("\n✅ 任务成功完成！")
        result = history.final_result()
        print(f"\n📊 搜索结果：\n{result}")
        
        # 显示访问的URL
        print(f"\n🌐 访问的网址：")
        for url in history.urls():
            print(f"  - {url}")
        
        return result
    else:
        print("\n❌ 任务未完成")
        errors = history.errors()
        if errors:
            print(f"错误信息：{errors}")
        return None


async def main():
    """主函数"""
    # 示例1：搜索Python教程
    await search_baidu("Python教程")
    
    # 示例2：搜索机器学习
    # await search_baidu("机器学习")
    
    # 示例3：搜索Web开发
    # await search_baidu("Web开发框架")


if __name__ == "__main__":
    print("🚀 启动浏览器自动化任务...")
    asyncio.run(main())
    print("\n✨ 所有任务完成！")
