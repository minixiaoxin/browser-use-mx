"""
无头模式对比演示
展示有头模式和无头模式的区别
"""

from browser_use import Agent, Browser, ChatBrowserUse
from dotenv import load_dotenv
import asyncio
import time

load_dotenv()


async def run_with_headless(headless: bool, task_name: str):
    """
    运行任务并测量性能
    
    Args:
        headless: 是否使用无头模式
        task_name: 任务名称
    """
    mode_name = "无头模式" if headless else "有头模式"
    print(f"\n{'='*60}")
    print(f"🚀 开始执行：{task_name} - {mode_name}")
    print(f"{'='*60}")
    
    # 创建浏览器
    browser = Browser(
        headless=headless,
        window_size={'width': 1920, 'height': 1080},
    )
    
    # 创建 Agent
    agent = Agent(
        task='访问百度首页，搜索"Python"，返回第一个结果的标题',
        llm=ChatBrowserUse(),
        browser=browser,
    )
    
    # 记录开始时间
    start_time = time.time()
    
    try:
        # 执行任务
        history = await agent.run(max_steps=8)
        
        # 记录结束时间
        end_time = time.time()
        duration = end_time - start_time
        
        # 显示结果
        print(f"\n📊 执行结果：")
        print(f"  - 模式：{mode_name}")
        print(f"  - 状态：{'✅ 成功' if history.is_done() else '❌ 失败'}")
        print(f"  - 执行时长：{duration:.2f} 秒")
        print(f"  - 步骤数：{history.number_of_steps()}")
        print(f"  - 访问的URL数：{len(history.urls())}")
        
        if history.is_done():
            result = history.final_result()
            print(f"  - 结果：{result[:100]}..." if len(result) > 100 else f"  - 结果：{result}")
        
        return {
            'mode': mode_name,
            'success': history.is_done(),
            'duration': duration,
            'steps': history.number_of_steps(),
            'urls': len(history.urls()),
        }
        
    except Exception as e:
        print(f"\n❌ 执行出错：{str(e)}")
        return {
            'mode': mode_name,
            'success': False,
            'error': str(e),
        }


async def compare_modes():
    """对比两种模式"""
    print("🎯 Browser-Use 无头模式对比演示")
    print("="*60)
    
    # 提示用户
    print("\n📝 说明：")
    print("  - 有头模式：会显示浏览器窗口，可以看到操作过程")
    print("  - 无头模式：后台运行，不显示窗口，速度更快")
    print("\n⏳ 准备开始测试...\n")
    
    input("按 Enter 键开始有头模式测试...")
    
    # 测试有头模式
    result_with_head = await run_with_headless(
        headless=False,
        task_name="百度搜索测试"
    )
    
    print("\n" + "="*60)
    input("按 Enter 键开始无头模式测试...")
    
    # 测试无头模式
    result_headless = await run_with_headless(
        headless=True,
        task_name="百度搜索测试"
    )
    
    # 显示对比结果
    print("\n" + "="*60)
    print("📊 性能对比结果")
    print("="*60)
    
    if result_with_head.get('success') and result_headless.get('success'):
        print(f"\n有头模式：")
        print(f"  - 执行时长：{result_with_head['duration']:.2f} 秒")
        print(f"  - 步骤数：{result_with_head['steps']}")
        
        print(f"\n无头模式：")
        print(f"  - 执行时长：{result_headless['duration']:.2f} 秒")
        print(f"  - 步骤数：{result_headless['steps']}")
        
        # 计算性能提升
        time_saved = result_with_head['duration'] - result_headless['duration']
        improvement = (time_saved / result_with_head['duration']) * 100
        
        print(f"\n💡 性能提升：")
        if time_saved > 0:
            print(f"  - 无头模式快了 {time_saved:.2f} 秒")
            print(f"  - 性能提升约 {improvement:.1f}%")
        else:
            print(f"  - 两种模式性能相近")
    
    print("\n" + "="*60)


async def interactive_demo():
    """交互式演示"""
    print("🎯 Browser-Use 无头模式交互演示")
    print("="*60)
    
    while True:
        print("\n请选择运行模式：")
        print("1. 有头模式（显示浏览器窗口）")
        print("2. 无头模式（后台运行）")
        print("3. 对比两种模式")
        print("4. 退出")
        
        choice = input("\n请输入选项 (1/2/3/4): ").strip()
        
        if choice == '1':
            await run_with_headless(headless=False, task_name="有头模式测试")
            
        elif choice == '2':
            await run_with_headless(headless=True, task_name="无头模式测试")
            
        elif choice == '3':
            await compare_modes()
            
        elif choice == '4':
            print("\n👋 再见！")
            break
            
        else:
            print("❌ 无效的选项！")


async def main():
    """主函数"""
    print("\n请选择演示模式：")
    print("1. 交互式演示（推荐）")
    print("2. 自动对比测试")
    
    choice = input("\n请输入选项 (1/2): ").strip()
    
    if choice == '1':
        await interactive_demo()
    elif choice == '2':
        await compare_modes()
    else:
        print("❌ 无效的选项！")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断程序")
    except Exception as e:
        print(f"\n❌ 程序出错：{str(e)}")
