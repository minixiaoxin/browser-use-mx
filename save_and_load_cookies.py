"""
保存和加载 Cookie（登录状态）
适用场景：生产环境、服务器部署
"""

from browser_use import Agent, Browser, ChatBrowserUse
from dotenv import load_dotenv
import asyncio
import os
import json

load_dotenv()


async def first_time_login(website_name: str, browser_data_dir: str = './browser_data'):
    """
    首次登录并保存状态
    
    Args:
        website_name: 网站名称（用于提示）
        browser_data_dir: 浏览器数据保存目录
    """
    print(f"🔐 首次登录 {website_name}")
    print("="*60)
    print(f"浏览器数据将保存到：{browser_data_dir}")
    print("="*60)
    
    browser = Browser(
        headless=False,  # 显示窗口，方便手动登录
        user_data_dir=browser_data_dir,
        window_size={'width': 1920, 'height': 1080},
    )
    
    agent = Agent(
        task=f'''
        1. 访问 {website_name}
        2. 等待用户手动登录（如果需要）
        3. 登录成功后，访问个人主页或主要页面
        4. 确认登录状态
        ''',
        llm=ChatBrowserUse(),
        browser=browser,
    )
    
    print(f"\n⏳ 浏览器将打开 {website_name}")
    print("📝 请在浏览器中完成登录...")
    print("💡 登录后，Agent 会自动继续执行")
    
    history = await agent.run(max_steps=20)
    
    print("\n" + "="*60)
    if history.is_done():
        print("✅ 登录状态已保存！")
        print(f"📁 保存位置：{browser_data_dir}")
        print("\n💡 下次运行时会自动使用这个登录状态")
        print(f"结果：{history.final_result()}")
    else:
        print("⚠️ 登录可能未完成")
        print("请检查浏览器中的登录状态")
    
    return history


async def use_saved_login(task: str, browser_data_dir: str = './browser_data', headless: bool = True):
    """
    使用保存的登录状态
    
    Args:
        task: 要执行的任务
        browser_data_dir: 浏览器数据目录
        headless: 是否使用无头模式
    """
    if not os.path.exists(browser_data_dir):
        print(f"❌ 错误：找不到保存的浏览器数据")
        print(f"目录：{browser_data_dir}")
        print("\n💡 请先运行首次登录流程")
        return None
    
    print(f"✅ 使用保存的登录状态")
    print("="*60)
    print(f"数据目录：{browser_data_dir}")
    print(f"无头模式：{'是' if headless else '否'}")
    print("="*60)
    
    browser = Browser(
        headless=headless,
        user_data_dir=browser_data_dir,
        window_size={'width': 1920, 'height': 1080},
    )
    
    agent = Agent(
        task=task,
        llm=ChatBrowserUse(),
        browser=browser,
    )
    
    print(f"\n🚀 开始执行任务...")
    print(f"任务：{task}")
    
    history = await agent.run(max_steps=15)
    
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
    
    print(f"\n📈 统计：")
    print(f"  - 步骤数：{history.number_of_steps()}")
    print(f"  - 时长：{history.total_duration_seconds():.2f} 秒")
    
    return history


async def check_login_status(browser_data_dir: str = './browser_data'):
    """
    检查登录状态是否有效
    
    Args:
        browser_data_dir: 浏览器数据目录
    """
    if not os.path.exists(browser_data_dir):
        print(f"❌ 未找到保存的登录状态")
        return False
    
    print(f"🔍 检查登录状态...")
    
    browser = Browser(
        headless=True,
        user_data_dir=browser_data_dir,
    )
    
    agent = Agent(
        task='检查当前登录状态，返回是否已登录',
        llm=ChatBrowserUse(),
        browser=browser,
    )
    
    history = await agent.run(max_steps=5)
    
    if history.is_done():
        print(f"✅ 登录状态检查完成")
        print(f"结果：{history.final_result()}")
        return True
    else:
        print(f"⚠️ 登录状态可能已过期")
        return False


async def interactive_mode():
    """交互式模式"""
    print("🎯 Cookie 管理 - 交互模式")
    print("="*60)
    
    # 默认数据目录
    default_dir = './browser_data'
    
    while True:
        print("\n请选择操作：")
        print("1. 首次登录（保存状态）")
        print("2. 使用保存的状态执行任务")
        print("3. 检查登录状态")
        print("4. 删除保存的状态")
        print("5. 退出")
        
        choice = input("\n请输入选项 (1/2/3/4/5): ").strip()
        
        if choice == '1':
            print("\n请选择网站：")
            print("1. GitHub")
            print("2. 淘宝")
            print("3. 其他网站")
            
            site_choice = input("请输入选项 (1/2/3): ").strip()
            
            if site_choice == '1':
                website = 'GitHub (github.com)'
                data_dir = './github_data'
            elif site_choice == '2':
                website = '淘宝 (taobao.com)'
                data_dir = './taobao_data'
            elif site_choice == '3':
                website = input("请输入网站名称: ").strip()
                data_dir = f'./{website.replace(" ", "_").lower()}_data'
            else:
                print("❌ 无效的选项！")
                continue
            
            await first_time_login(website, data_dir)
            
        elif choice == '2':
            # 列出可用的数据目录
            data_dirs = [d for d in os.listdir('.') if d.endswith('_data') and os.path.isdir(d)]
            
            if not data_dirs:
                print("\n❌ 没有找到保存的登录状态")
                print("💡 请先执行首次登录")
                continue
            
            print("\n可用的登录状态：")
            for i, dir_name in enumerate(data_dirs, 1):
                print(f"{i}. {dir_name}")
            
            dir_choice = input(f"\n请选择 (1-{len(data_dirs)}): ").strip()
            
            try:
                dir_index = int(dir_choice) - 1
                if 0 <= dir_index < len(data_dirs):
                    data_dir = data_dirs[dir_index]
                    
                    task = input("\n请输入任务描述: ").strip()
                    if task:
                        headless_choice = input("使用无头模式？(y/n): ").strip().lower()
                        headless = headless_choice == 'y'
                        
                        await use_saved_login(task, data_dir, headless)
                    else:
                        print("❌ 任务不能为空！")
                else:
                    print("❌ 无效的选项！")
            except ValueError:
                print("❌ 请输入有效的数字！")
                
        elif choice == '3':
            data_dirs = [d for d in os.listdir('.') if d.endswith('_data') and os.path.isdir(d)]
            
            if not data_dirs:
                print("\n❌ 没有找到保存的登录状态")
                continue
            
            print("\n检查登录状态：")
            for data_dir in data_dirs:
                print(f"\n📁 {data_dir}:")
                await check_login_status(data_dir)
                
        elif choice == '4':
            data_dirs = [d for d in os.listdir('.') if d.endswith('_data') and os.path.isdir(d)]
            
            if not data_dirs:
                print("\n❌ 没有找到保存的登录状态")
                continue
            
            print("\n可用的登录状态：")
            for i, dir_name in enumerate(data_dirs, 1):
                print(f"{i}. {dir_name}")
            
            dir_choice = input(f"\n请选择要删除的 (1-{len(data_dirs)}): ").strip()
            
            try:
                dir_index = int(dir_choice) - 1
                if 0 <= dir_index < len(data_dirs):
                    data_dir = data_dirs[dir_index]
                    confirm = input(f"确认删除 {data_dir}？(yes/no): ").strip().lower()
                    
                    if confirm == 'yes':
                        import shutil
                        shutil.rmtree(data_dir)
                        print(f"✅ 已删除 {data_dir}")
                    else:
                        print("❌ 已取消")
                else:
                    print("❌ 无效的选项！")
            except ValueError:
                print("❌ 请输入有效的数字！")
                
        elif choice == '5':
            print("\n👋 再见！")
            break
            
        else:
            print("❌ 无效的选项！")


async def main():
    """主函数"""
    await interactive_mode()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断程序")
    except Exception as e:
        print(f"\n❌ 程序出错：{str(e)}")
        import traceback
        traceback.print_exc()
