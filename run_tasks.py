"""
任务执行器 - 增强版
用于快速执行 YAML 任务文件，支持授权配置和人工确认
"""

import asyncio
import sys
import yaml
import os
from pathlib import Path
from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatBrowserUse, Tools, ActionResult

load_dotenv()


# ============================================================
# 人工确认工具（从 form_with_confirmation.py 集成）
# ============================================================

def create_confirmation_tools():
    """创建人工确认工具集"""
    tools = Tools()
    
    @tools.action('等待用户确认表单内容')
    def confirm_form_content(form_summary: str) -> ActionResult:
        """
        显示表单内容并等待用户确认
        
        Args:
            form_summary: 表单内容摘要
        
        Returns:
            确认结果
        """
        print(f"\n{'='*60}")
        print(f"📋 表单内容确认")
        print(f"{'='*60}")
        print(f"\n已填写的内容：")
        print(f"{form_summary}")
        print(f"\n💡 请在浏览器中检查表单内容是否正确")
        print(f"{'='*60}")
        
        while True:
            print(f"\n请选择操作：")
            print(f"  y - 内容正确，继续")
            print(f"  n - 取消任务")
            print(f"  e - 需要修改")
            
            choice = input("\n请输入选项 (y/n/e): ").strip().lower()
            
            if choice == 'y':
                print("\n✅ 用户确认内容正确")
                return ActionResult(
                    extracted_content="用户确认表单内容正确，可以继续",
                    success=True
                )
            elif choice == 'n':
                print("\n❌ 用户取消任务")
                return ActionResult(
                    extracted_content="用户取消了任务",
                    error="用户取消",
                    success=False,
                    is_done=True
                )
            elif choice == 'e':
                print("\n✏️ 请在浏览器中修改内容...")
                input("修改完成后按 Enter 继续...")
                
                changes = input("请简要描述修改内容（可选）: ").strip()
                
                print("\n✅ 修改完成")
                return ActionResult(
                    extracted_content=f"用户已修改内容：{changes if changes else '未描述'}",
                    success=True
                )
            else:
                print("❌ 无效的选项，请输入 y、n 或 e")
    
    @tools.action('最终确认提交')
    def confirm_final_submit() -> ActionResult:
        """
        最终确认是否提交表单
        
        Returns:
            确认结果
        """
        print(f"\n{'='*60}")
        print(f"⚠️  最终确认")
        print(f"{'='*60}")
        print(f"\n即将提交表单！")
        print(f"这是最后一次检查机会")
        print(f"\n💡 请再次确认所有内容无误")
        print(f"{'='*60}")
        
        while True:
            choice = input("\n确认提交？(yes/no): ").strip().lower()
            
            if choice == 'yes':
                print("\n✅ 确认提交表单")
                return ActionResult(
                    extracted_content="用户最终确认提交",
                    success=True
                )
            elif choice == 'no':
                print("\n❌ 取消提交")
                return ActionResult(
                    extracted_content="用户取消提交",
                    error="用户取消提交",
                    success=False,
                    is_done=True
                )
            else:
                print("❌ 请输入 yes 或 no")
    
    @tools.action('暂停等待用户操作')
    def pause_for_user(instruction: str) -> ActionResult:
        """
        暂停任务，等待用户手动操作
        
        Args:
            instruction: 给用户的操作指示
        
        Returns:
            操作结果
        """
        print(f"\n{'='*60}")
        print(f"⏸️  任务暂停")
        print(f"{'='*60}")
        print(f"\n📝 请执行以下操作：")
        print(f"   {instruction}")
        print(f"\n💡 在浏览器中完成操作后继续")
        print(f"{'='*60}")
        
        input("\n✅ 完成后按 Enter 继续...")
        
        return ActionResult(
            extracted_content="用户已完成手动操作",
            success=True
        )
    
    return tools


def get_chrome_paths():
    """获取 Chrome 路径（根据操作系统）"""
    system = sys.platform
    
    if system == 'win32':
        chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        user_data_dir = os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data')
    elif system == 'darwin':
        chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        user_data_dir = os.path.expanduser('~/Library/Application Support/Google/Chrome')
    else:
        chrome_path = '/usr/bin/google-chrome'
        user_data_dir = os.path.expanduser('~/.config/google-chrome')
    
    return chrome_path, user_data_dir


def list_auth_profiles():
    """列出可用的授权配置"""
    profiles = []
    
    # 1. 检查保存的浏览器数据目录
    data_dirs = [d for d in os.listdir('.') if d.endswith('_data') and os.path.isdir(d)]
    for data_dir in data_dirs:
        profiles.append({
            'type': 'saved_cookies',
            'name': data_dir.replace('_data', '').replace('_', ' ').title(),
            'path': data_dir,
            'description': f'保存的Cookie ({data_dir})'
        })
    
    # 2. 检查真实浏览器配置
    chrome_path, user_data_dir = get_chrome_paths()
    if os.path.exists(chrome_path) and os.path.exists(user_data_dir):
        profiles.append({
            'type': 'real_browser',
            'name': 'Chrome Default',
            'path': user_data_dir,
            'profile': 'Default',
            'executable': chrome_path,
            'description': '真实Chrome浏览器 (Default配置)'
        })
        
        # 检查其他配置文件
        for i in range(1, 6):
            profile_dir = os.path.join(user_data_dir, f'Profile {i}')
            if os.path.exists(profile_dir):
                profiles.append({
                    'type': 'real_browser',
                    'name': f'Chrome Profile {i}',
                    'path': user_data_dir,
                    'profile': f'Profile {i}',
                    'executable': chrome_path,
                    'description': f'真实Chrome浏览器 (Profile {i})'
                })
    
    # 3. 无授权（默认）
    profiles.insert(0, {
        'type': 'none',
        'name': '无授权',
        'description': '使用全新浏览器实例（无登录状态）'
    })
    
    return profiles


def create_browser_with_auth(auth_config: dict, headless: bool = False):
    """
    根据授权配置创建浏览器实例
    
    Args:
        auth_config: 授权配置字典
        headless: 是否无头模式
    
    Returns:
        Browser 实例
    """
    if auth_config['type'] == 'none':
        # 无授权
        return Browser(
            headless=headless,
            window_size={'width': 1920, 'height': 1080},
        )
    
    elif auth_config['type'] == 'saved_cookies':
        # 使用保存的Cookie
        return Browser(
            headless=headless,
            user_data_dir=auth_config['path'],
            window_size={'width': 1920, 'height': 1080},
        )
    
    elif auth_config['type'] == 'real_browser':
        # 使用真实浏览器配置
        return Browser(
            headless=headless,
            executable_path=auth_config['executable'],
            user_data_dir=auth_config['path'],
            profile_directory=auth_config['profile'],
            window_size={'width': 1920, 'height': 1080},
        )
    
    else:
        # 默认
        return Browser(
            headless=headless,
            window_size={'width': 1920, 'height': 1080},
        )


async def run_yaml_task(yaml_file: str, headless: bool = False, auth_config: dict = None, use_confirmation: bool = False):
    """
    执行单个YAML任务文件
    
    Args:
        yaml_file: YAML任务文件路径
        headless: 是否无头模式运行
        auth_config: 授权配置字典
        use_confirmation: 是否启用人工确认功能
    """
    # 读取任务文件
    task_path = Path(yaml_file)
    if not task_path.exists():
        print(f"❌ 文件不存在：{yaml_file}")
        return None
    
    print(f"\n{'='*60}")
    print(f"📋 加载任务文件：{task_path.name}")
    print(f"{'='*60}")
    
    with open(task_path, 'r', encoding='utf-8') as f:
        task_data = yaml.safe_load(f)
    
    task_name = task_data.get('name', '未命名任务')
    task_desc = task_data.get('task', '')
    max_steps = task_data.get('max_steps', 15)
    
    print(f"\n📝 任务名称：{task_name}")
    print(f"📄 任务描述：\n{task_desc}")
    print(f"🔢 最大步骤：{max_steps}")
    
    # 显示是否启用确认功能
    if use_confirmation:
        print(f"\n🔐 人工确认：已启用")
        print(f"   - 填写完成后会等待确认")
        print(f"   - 提交前会最终确认")
    
    # 显示授权配置
    if auth_config:
        print(f"\n🔐 授权配置：{auth_config['name']}")
        print(f"   说明：{auth_config['description']}")
        
        if auth_config['type'] == 'real_browser':
            print(f"\n⚠️ 重要：使用真实浏览器配置")
            print(f"   请确保已完全关闭 Chrome 浏览器！")
            input("   准备好后按 Enter 继续...")
    
    print(f"\n{'='*60}")
    print("🚀 开始执行任务...")
    print(f"{'='*60}\n")
    
    # 创建浏览器配置
    if auth_config:
        browser = create_browser_with_auth(auth_config, headless)
    else:
        browser = Browser(
            headless=headless,
            window_size={'width': 1920, 'height': 1080},
        )
    
    # 如果启用确认功能，增强任务描述
    if use_confirmation:
        enhanced_task = f'''{task_desc}

重要：填写完成后的确认流程
1. 填写完所有字段后，使用 confirm_form_content 工具
2. 传入参数 form_summary，包含所有已填写内容的摘要
3. 等待工具返回结果
4. 如果返回 success=False，立即停止任务，不要提交
5. 如果返回 success=True，使用 confirm_final_submit 工具进行最终确认
6. 只有在 confirm_final_submit 返回 success=True 时才能点击提交按钮

严格禁止：
- 不要在未调用 confirm_form_content 的情况下提交
- 不要在未调用 confirm_final_submit 的情况下提交
- 不要在用户取消（success=False）后继续执行
- 不要跳过任何确认步骤
'''
        task_to_run = enhanced_task
        tools = create_confirmation_tools()
    else:
        task_to_run = task_desc
        tools = None
    
    # 创建Agent
    agent = Agent(
        task=task_to_run,
        llm=ChatBrowserUse(),
        browser=browser,
        tools=tools,
    )
    
    try:
        # 执行任务
        history = await agent.run(max_steps=max_steps)
        
        # 显示结果
        print(f"\n{'='*60}")
        print("📊 任务执行结果")
        print(f"{'='*60}")
        
        if history.is_done():
            print("\n✅ 任务成功完成！")
            result = history.final_result()
            print(f"\n📄 结果：\n{result}")
        else:
            print("\n⚠️ 任务未完成")
            errors = history.errors()
            if errors:
                print(f"\n❌ 错误信息：")
                for i, error in enumerate(errors, 1):
                    if error:
                        print(f"  {i}. {error}")
        
        # 显示统计信息
        print(f"\n📈 执行统计：")
        print(f"  - 总步骤数：{history.number_of_steps()}")
        print(f"  - 执行时长：{history.total_duration_seconds():.2f} 秒")
        print(f"  - 访问的URL数：{len(history.urls())}")
        
        # 显示访问的URL
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


async def run_multiple_tasks(task_files: list, headless: bool = False, auth_config: dict = None, use_confirmation: bool = False):
    """
    顺序执行多个任务
    
    Args:
        task_files: 任务文件路径列表
        headless: 是否无头模式运行
        auth_config: 授权配置字典
        use_confirmation: 是否启用人工确认功能
    """
    print(f"\n🎯 准备执行 {len(task_files)} 个任务")
    
    results = []
    for i, task_file in enumerate(task_files, 1):
        print(f"\n{'#'*60}")
        print(f"任务 {i}/{len(task_files)}")
        print(f"{'#'*60}")
        
        result = await run_yaml_task(task_file, headless, auth_config, use_confirmation)
        results.append({
            'file': task_file,
            'success': result.is_done() if result else False,
            'result': result
        })
        
        # 任务之间稍作延迟
        if i < len(task_files):
            print("\n⏳ 等待3秒后执行下一个任务...")
            await asyncio.sleep(3)
    
    # 显示总结
    print(f"\n{'='*60}")
    print("📊 所有任务执行完成")
    print(f"{'='*60}")
    
    success_count = sum(1 for r in results if r['success'])
    fail_count = len(results) - success_count
    
    print(f"\n✅ 成功：{success_count}/{len(results)}")
    print(f"❌ 失败：{fail_count}/{len(results)}")
    
    print(f"\n详细结果：")
    for i, r in enumerate(results, 1):
        status = "✅" if r['success'] else "❌"
        print(f"  {i}. {status} {Path(r['file']).name}")


def list_available_tasks():
    """列出所有可用的任务文件"""
    task_dir = Path('tests/agent_tasks')
    if not task_dir.exists():
        print("❌ 任务目录不存在：tests/agent_tasks")
        return []
    
    yaml_files = list(task_dir.glob('*.yaml'))
    
    if not yaml_files:
        print("⚠️ 没有找到任务文件")
        return []
    
    print(f"\n📋 找到 {len(yaml_files)} 个任务文件：")
    print(f"{'='*60}")
    
    for i, file in enumerate(yaml_files, 1):
        # 读取任务名称
        try:
            with open(file, 'r', encoding='utf-8') as f:
                task_data = yaml.safe_load(f)
                task_name = task_data.get('name', '未命名')
        except:
            task_name = '读取失败'
        
        print(f"{i}. {file.name}")
        print(f"   名称：{task_name}")
    
    print(f"{'='*60}")
    return yaml_files


def main():
    """主函数"""
    print("🤖 Browser-Use 任务执行器（增强版）")
    print("="*60)
    
    # 解析命令行参数
    if len(sys.argv) > 1:
        # 命令行模式
        task_file = sys.argv[1]
        headless = '--headless' in sys.argv
        
        print(f"\n📂 执行任务文件：{task_file}")
        if headless:
            print("🔇 无头模式")
        
        asyncio.run(run_yaml_task(task_file, headless))
    else:
        # 交互模式
        print("\n请选择运行模式：")
        print("1. 列出所有可用任务")
        print("2. 执行单个任务")
        print("3. 执行所有任务")
        print("4. 管理授权配置")
        print("5. 退出")
        
        choice = input("\n请输入选项 (1/2/3/4/5): ").strip()
        
        if choice == '1':
            list_available_tasks()
            
        elif choice == '2':
            yaml_files = list_available_tasks()
            if yaml_files:
                try:
                    idx = int(input("\n请输入任务编号: ").strip()) - 1
                    if 0 <= idx < len(yaml_files):
                        # 选择授权配置
                        auth_config = select_auth_profile()
                        
                        # 选择是否启用人工确认
                        use_confirmation = input("\n是否启用人工确认？(y/n): ").strip().lower() == 'y'
                        if use_confirmation:
                            print("✅ 已启用人工确认功能")
                            print("   - 填写完成后会等待你确认")
                            print("   - 提交前会最终确认")
                        
                        # 选择无头模式
                        headless = input("\n是否使用无头模式？(y/n): ").strip().lower() == 'y'
                        
                        # 执行任务
                        asyncio.run(run_yaml_task(str(yaml_files[idx]), headless, auth_config, use_confirmation))
                    else:
                        print("❌ 无效的编号！")
                except ValueError:
                    print("❌ 请输入有效的数字！")
                    
        elif choice == '3':
            yaml_files = list_available_tasks()
            if yaml_files:
                # 选择授权配置
                auth_config = select_auth_profile()
                
                # 选择是否启用人工确认
                use_confirmation = input("\n是否启用人工确认？(y/n): ").strip().lower() == 'y'
                if use_confirmation:
                    print("✅ 已启用人工确认功能")
                
                # 选择无头模式
                headless = input("\n是否使用无头模式？(y/n): ").strip().lower() == 'y'
                
                confirm = input(f"\n确认执行所有 {len(yaml_files)} 个任务？(y/n): ").strip().lower()
                if confirm == 'y':
                    asyncio.run(run_multiple_tasks([str(f) for f in yaml_files], headless, auth_config, use_confirmation))
                else:
                    print("❌ 已取消")
                    
        elif choice == '4':
            manage_auth_profiles()
            
        elif choice == '5':
            print("\n👋 再见！")
            
        else:
            print("❌ 无效的选项！")


def select_auth_profile():
    """选择授权配置"""
    profiles = list_auth_profiles()
    
    if not profiles:
        print("\n⚠️ 没有找到可用的授权配置")
        return None
    
    print(f"\n🔐 选择授权配置：")
    print("="*60)
    
    for i, profile in enumerate(profiles, 1):
        icon = "🌐" if profile['type'] == 'none' else "🔑"
        print(f"{i}. {icon} {profile['name']}")
        print(f"   {profile['description']}")
    
    print("="*60)
    
    try:
        choice = input(f"\n请选择 (1-{len(profiles)}, 直接回车使用默认): ").strip()
        
        if not choice:
            # 默认使用第一个（无授权）
            return profiles[0]
        
        idx = int(choice) - 1
        if 0 <= idx < len(profiles):
            selected = profiles[idx]
            print(f"\n✅ 已选择：{selected['name']}")
            return selected
        else:
            print("❌ 无效的选项，使用默认配置")
            return profiles[0]
    except ValueError:
        print("❌ 无效的输入，使用默认配置")
        return profiles[0]


def manage_auth_profiles():
    """管理授权配置"""
    print("\n🔐 授权配置管理")
    print("="*60)
    
    while True:
        print("\n请选择操作：")
        print("1. 查看所有授权配置")
        print("2. 创建新的Cookie配置")
        print("3. 删除Cookie配置")
        print("4. 测试授权配置")
        print("5. 返回主菜单")
        
        choice = input("\n请输入选项 (1/2/3/4/5): ").strip()
        
        if choice == '1':
            # 查看所有配置
            profiles = list_auth_profiles()
            print(f"\n📋 找到 {len(profiles)} 个授权配置：")
            print("="*60)
            
            for i, profile in enumerate(profiles, 1):
                icon = "🌐" if profile['type'] == 'none' else "🔑"
                print(f"\n{i}. {icon} {profile['name']}")
                print(f"   类型：{profile['type']}")
                print(f"   说明：{profile['description']}")
                if profile['type'] == 'saved_cookies':
                    print(f"   路径：{profile['path']}")
                elif profile['type'] == 'real_browser':
                    print(f"   配置：{profile['profile']}")
            
            print("="*60)
            
        elif choice == '2':
            # 创建新的Cookie配置
            print("\n📝 创建新的Cookie配置")
            print("="*60)
            
            name = input("请输入配置名称（如：taobao, github）: ").strip()
            if name:
                data_dir = f'./{name}_data'
                
                if os.path.exists(data_dir):
                    print(f"⚠️ 配置 {name} 已存在")
                else:
                    print(f"\n💡 将创建配置：{name}")
                    print(f"   数据目录：{data_dir}")
                    print("\n📝 接下来会打开浏览器，请手动登录需要的网站")
                    
                    confirm = input("\n确认创建？(y/n): ").strip().lower()
                    if confirm == 'y':
                        # 创建目录
                        os.makedirs(data_dir, exist_ok=True)
                        
                        print(f"\n✅ 配置目录已创建：{data_dir}")
                        print(f"💡 现在可以使用此配置执行任务")
                        print(f"   首次使用时会打开浏览器让你登录")
                    else:
                        print("❌ 已取消")
            else:
                print("❌ 名称不能为空！")
                
        elif choice == '3':
            # 删除Cookie配置
            data_dirs = [d for d in os.listdir('.') if d.endswith('_data') and os.path.isdir(d)]
            
            if not data_dirs:
                print("\n⚠️ 没有找到可删除的Cookie配置")
                continue
            
            print("\n🗑️ 删除Cookie配置")
            print("="*60)
            
            for i, data_dir in enumerate(data_dirs, 1):
                print(f"{i}. {data_dir}")
            
            print("="*60)
            
            try:
                idx = int(input(f"\n请选择要删除的配置 (1-{len(data_dirs)}): ").strip()) - 1
                if 0 <= idx < len(data_dirs):
                    data_dir = data_dirs[idx]
                    confirm = input(f"\n⚠️ 确认删除 {data_dir}？(yes/no): ").strip().lower()
                    
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
                
        elif choice == '4':
            # 测试授权配置
            print("\n🧪 测试授权配置")
            print("="*60)
            
            profile = select_auth_profile()
            if profile:
                print(f"\n测试配置：{profile['name']}")
                print("将打开浏览器访问百度首页...")
                
                async def test_auth():
                    browser = create_browser_with_auth(profile, headless=False)
                    agent = Agent(
                        task='访问百度首页，返回页面标题',
                        llm=ChatBrowserUse(),
                        browser=browser,
                    )
                    history = await agent.run(max_steps=5)
                    if history.is_done():
                        print(f"\n✅ 测试成功！")
                        print(f"结果：{history.final_result()}")
                    else:
                        print(f"\n⚠️ 测试未完成")
                
                asyncio.run(test_auth())
                
        elif choice == '5':
            break
            
        else:
            print("❌ 无效的选项！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断程序")
    except Exception as e:
        print(f"\n❌ 程序出错：{str(e)}")
        import traceback
        traceback.print_exc()
