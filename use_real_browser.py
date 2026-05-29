"""
使用真实浏览器配置（保留登录状态）
适用场景：本地开发、已在浏览器中登录的网站
"""

from browser_use import Agent, Browser, ChatBrowserUse
from dotenv import load_dotenv
import asyncio
import os
import sys

load_dotenv()


def get_chrome_paths():
    """获取 Chrome 路径（根据操作系统）"""
    system = sys.platform
    
    if system == 'win32':
        # Windows
        chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        user_data_dir = os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data')
    elif system == 'darwin':
        # macOS
        chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        user_data_dir = os.path.expanduser('~/Library/Application Support/Google/Chrome')
    else:
        # Linux
        chrome_path = '/usr/bin/google-chrome'
        user_data_dir = os.path.expanduser('~/.config/google-chrome')
    
    return chrome_path, user_data_dir


async def use_real_browser(task: str, profile: str = 'Default'):
    """
    使用真实浏览器配置执行任务
    
    Args:
        task: 要执行的任务
        profile: Chrome 配置文件名（Default, Profile 1, Profile 2 等）
    """
    chrome_path, user_data_dir = get_chrome_paths()
    
    print("🌐 使用真实浏览器配置")
    print("="*60)
    print(f"Chrome 路径: {chrome_path}")
    print(f"用户数据目录: {user_data_dir}")
    print(f"配置文件: {profile}")
    print("="*60)
    
    # 检查 Chrome 是否存在
    if not os.path.exists(chrome_path):
        print(f"\n❌ 错误：找不到 Chrome 浏览器")
        print(f"路径：{chrome_path}")
        print("\n💡 解决方案：")
        print("1. 安装 Google Chrome")
        print("2. 或修改脚本中的 chrome_path 为你的 Chrome 路径")
        return
    
    # 检查用户数据目录是否存在
    if not os.path.exists(user_data_dir):
        print(f"\n❌ 错误：找不到用户数据目录")
        print(f"路径：{user_data_dir}")
        return
    
    print("\n⚠️ 重要提示：")
    print("1. 请先在 Chrome 中登录需要的网站")
    print("2. 然后完全关闭 Chrome 浏览器")
    print("3. 确保任务管理器中没有 chrome.exe 进程")
    
    input("\n✅ 准备好后按 Enter 继续...")
    
    try:
        # 创建浏览器实例
        browser = Browser(
            executable_path=chrome_path,
            user_data_dir=user_data_dir,
            profile_directory=profile,
            headless=False,  # 显示窗口
            window_size={'width': 1920, 'height': 1080},
        )
        
        # 创建 Agent
        agent = Agent(
            task=task,
            llm=ChatBrowserUse(),
            browser=browser,
        )
        
        print(f"\n🚀 开始执行任务...")
        print(f"任务：{task}")
        print("="*60)
        
        # 执行任务
        history = await agent.run(max_steps=15)
        
        # 显示结果
        print("\n" + "="*60)
        print("📊 执行结果")
        print("="*60)
        
        if history.is_done():
            print("\n✅ 任务成功完成！")
            result = history.final_result()
            print(f"\n📄 结果：\n{result}")
        else:
            print("\n⚠️ 任务未完成")
            errors = history.errors()
            if errors:
                print(f"\n❌ 错误：")
                for i, error in enumerate(errors, 1):
                    if error:
                        print(f"  {i}. {error}")
        
        # 显示统计
        print(f"\n📈 统计信息：")
        print(f"  - 执行步骤：{history.number_of_steps()}")
        print(f"  - 执行时长：{history.total_duration_seconds():.2f} 秒")
        print(f"  - 访问URL数：{len(history.urls())}")
        
        if history.urls():
            print(f"\n🌐 访问的网址：")
            for url in history.urls():
                print(f"  - {url}")
        
        return history
        
    except Exception as e:
        print(f"\n❌ 执行出错：{str(e)}")
        import traceback
        traceback.print_exc()
        return None


async def interactive_mode():
    """交互式模式"""
    print("🎯 使用真实浏览器配置 - 交互模式")
    print("="*60)
    
    while True:
        print("\n请选择操作：")
        print("1. 执行自定义任务")
        print("2. 测试 GitHub（需要已登录）")
        print("3. 测试淘宝（需要已登录）")
        print("4. 测试百度（无需登录）")
        print("5. 退出")
        
        choice = input("\n请输入选项 (1/2/3/4/5): ").strip()
        
        if choice == '1':
            task = input("\n请输入任务描述: ").strip()
            if task:
                await use_real_browser(task)
            else:
                print("❌ 任务不能为空！")
                
        elif choice == '2':
            task = '''
            1. 访问 GitHub
            2. 检查是否已登录
            3. 如果已登录，访问个人主页
            4. 返回用户名和最近的仓库
            '''
            await use_real_browser(task)
            
        elif choice == '3':
            task = '''
            1. 访问淘宝
            2. 检查是否已登录
            3. 如果已登录，搜索"机械键盘"
            4. 返回前3个商品的名称和价格
            '''
            await use_real_browser(task)
            
        elif choice == '4':
            task = '''
            1. 访问百度
            2. 搜索"Python教程"
            3. 返回前5个搜索结果的标题
            '''
            await use_real_browser(task)
            
        elif choice == '5':
            print("\n👋 再见！")
            break
            
        else:
            print("❌ 无效的选项！")


async def main():
    """主函数"""
    print("\n请选择运行模式：")
    print("1. 交互模式（推荐）")
    print("2. 直接执行任务")
    
    choice = input("\n请输入选项 (1/2): ").strip()
    
    if choice == '1':
        await interactive_mode()
    elif choice == '2':
        task = input("\n请输入任务描述: ").strip()
        if task:
            await use_real_browser(task)
        else:
            print("❌ 任务不能为空！")
    else:
        print("❌ 无效的选项！")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断程序")
    except Exception as e:
        print(f"\n❌ 程序出错：{str(e)}")
        import traceback
        traceback.print_exc()
