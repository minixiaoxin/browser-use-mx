"""
表单填写任务（带人工确认）
功能：填写表单后等待用户确认，防止自动提交
"""

from browser_use import Agent, Browser, Tools, ChatBrowserUse, ActionResult
from dotenv import load_dotenv
import asyncio

load_dotenv()

# 创建自定义工具
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
                success=False
            )
        elif choice == 'e':
            print("\n✏️ 请在浏览器中修改内容...")
            input("修改完成后按 Enter 继续...")
            
            # 让用户描述修改了什么
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
                success=False
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


async def run_form_task(task_description: str, form_url: str = None):
    """
    运行表单填写任务（带确认）
    
    Args:
        task_description: 任务描述
        form_url: 表单URL（可选）
    """
    print("🚀 启动表单填写任务（带确认）")
    print("="*60)
    
    browser = Browser(
        headless=False,  # 必须显示窗口
        window_size={'width': 1920, 'height': 1080},
    )
    
    # 构建完整任务
    full_task = f'''
任务：{task_description}

重要规则：
1. 填写完所有字段后，必须使用 confirm_form_content 工具
2. 传入参数 form_summary，包含所有填写的内容
3. 等待工具返回结果
4. 如果返回 success=False，立即停止任务
5. 如果返回 success=True，继续下一步
6. 在提交前，必须使用 confirm_final_submit 工具
7. 只有在该工具返回 success=True 时才能提交
8. 如果返回 success=False，立即停止任务，不要提交

严格禁止：
- 不要在未确认的情况下提交表单
- 不要跳过确认步骤
- 不要在用户取消后继续执行
'''
    
    if form_url:
        full_task = f"1. 访问 {form_url}\n2. " + full_task
    
    print(f"\n📝 任务描述：")
    print(f"{task_description}")
    print(f"\n{'='*60}")
    print("🚀 开始执行...")
    print(f"{'='*60}\n")
    
    agent = Agent(
        task=full_task,
        llm=ChatBrowserUse(),
        browser=browser,
        tools=tools,
    )
    
    try:
        history = await agent.run(max_steps=30)
        
        print(f"\n{'='*60}")
        print("📊 任务执行结果")
        print(f"{'='*60}")
        
        if history.is_done():
            print("\n✅ 任务成功完成！")
            result = history.final_result()
            print(f"\n📄 结果：\n{result}")
        else:
            print("\n⚠️ 任务未完成")
            print("可能原因：")
            print("  - 用户取消了操作")
            print("  - 任务执行出错")
            print("  - 达到最大步骤数")
            
            errors = history.errors()
            if errors:
                print(f"\n❌ 错误信息：")
                for i, error in enumerate(errors, 1):
                    if error:
                        print(f"  {i}. {error}")
        
        print(f"\n📈 执行统计：")
        print(f"  - 总步骤数：{history.number_of_steps()}")
        print(f"  - 执行时长：{history.total_duration_seconds():.2f} 秒")
        
        return history
        
    except Exception as e:
        print(f"\n❌ 执行出错：{str(e)}")
        import traceback
        traceback.print_exc()
        return None


async def interactive_mode():
    """交互式模式"""
    print("🎯 表单填写任务（带确认）- 交互模式")
    print("="*60)
    
    while True:
        print("\n请选择任务类型：")
        print("1. 自定义任务")
        print("2. 示例：联系表单")
        print("3. 示例：注册表单")
        print("4. 退出")
        
        choice = input("\n请输入选项 (1/2/3/4): ").strip()
        
        if choice == '1':
            print("\n📝 自定义任务")
            print("-"*60)
            
            form_url = input("表单URL（可选，直接回车跳过）: ").strip()
            task = input("任务描述: ").strip()
            
            if task:
                await run_form_task(
                    task_description=task,
                    form_url=form_url if form_url else None
                )
            else:
                print("❌ 任务描述不能为空！")
                
        elif choice == '2':
            print("\n📝 示例：联系表单")
            await run_form_task(
                task_description='''
                填写联系表单：
                - 姓名：张三
                - 邮箱：zhangsan@example.com
                - 电话：13800138000
                - 消息：这是一条测试消息
                
                填写完成后等待确认，确认后提交
                ''',
                form_url='https://example.com/contact'
            )
            
        elif choice == '3':
            print("\n📝 示例：注册表单")
            await run_form_task(
                task_description='''
                填写注册表单：
                - 用户名：testuser
                - 邮箱：test@example.com
                - 密码：Test123456
                - 确认密码：Test123456
                
                填写完成后等待确认，确认后提交
                ''',
                form_url='https://example.com/register'
            )
            
        elif choice == '4':
            print("\n👋 再见！")
            break
            
        else:
            print("❌ 无效的选项！")


async def main():
    """主函数"""
    print("\n请选择运行模式：")
    print("1. 交互模式（推荐）")
    print("2. 直接运行示例")
    
    choice = input("\n请输入选项 (1/2): ").strip()
    
    if choice == '1':
        await interactive_mode()
    elif choice == '2':
        # 直接运行示例
        await run_form_task(
            task_description='''
            访问百度首页，搜索"Python教程"
            在搜索前使用 confirm_form_content 工具确认
            确认后再执行搜索
            ''',
            form_url='https://www.baidu.com'
        )
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
        import traceback
        traceback.print_exc()
