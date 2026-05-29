#!/usr/bin/env python3
"""
Quick start script for running browser automation tasks with OpenRouter
"""

from browser_use import Agent, ChatOpenRouter
from dotenv import load_dotenv
import asyncio
import os

def run_task_example():
    """Run a simple example task to demonstrate OpenRouter integration"""
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY not found in environment variables")
        print("Please add your OpenRouter API key to the .env file")
        print("Example .env content:")
        print("OPENROUTER_API_KEY=your_actual_api_key_here")
        return
    
    print("🚀 Browser Automation with OpenRouter - Quick Start")
    print("=" * 55)
    
    # Define a simple task
    task = input("Enter your automation task (or press Enter for default): ").strip()
    if not task:
        task = "Search for 'Python web scraping tutorial 2025' on Google and summarize the top 3 results"
    
    print(f"\n📋 Task: {task}")
    print("🤖 Initializing agent with OpenRouter...")
    
    # Configure the LLM to use OpenRouter
    llm = ChatOpenRouter(
        model='openai/gpt-4o-mini',  # You can change this to any OpenRouter model
        api_key=api_key,
        temperature=0.1,
    )
    
    # Create the agent
    agent = Agent(
        task=task,
        llm=llm,
        max_steps=20,
        use_vision=False,  # Set to True if you want to enable screenshots
    )
    
    print(f"✅ Agent created with model: {llm.model}")
    print("🚀 Starting automation task...\n")
    
    # Run the agent
    try:
        history = asyncio.run(agent.run())
        
        print(f"\n✅ Task completed successfully!")
        print(f"📊 Stats: {len(history.history)} steps taken")
        
        if history.final_result():
            print(f"📋 Final result: {history.final_result()}")
        else:
            print("⚠️ No final result available")
            
    except KeyboardInterrupt:
        print("\n⚠️ Task interrupted by user")
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")

def list_common_tasks():
    """Display common automation tasks users might want to try"""
    common_tasks = [
        "Search for 'latest AI news' on Google and summarize top results",
        "Go to https://news.ycombinator.com and find the top 5 stories",
        "Search for 'Python data science tutorial' and extract top resources",
        "Go to a shopping site and search for 'laptop deals'",
        "Find contact information for a company on their website",
        "Extract product prices from an e-commerce site",
        "Search for flights between two cities on a travel site",
        "Find and extract business hours from a local business website"
    ]
    
    print("\n💡 Common automation tasks you can try:")
    for i, task in enumerate(common_tasks, 1):
        print(f"  {i}. {task}")

if __name__ == "__main__":
    print("Browser Automation with OpenRouter")
    print("=" * 35)
    
    list_common_tasks()
    print()
    run_task_example()
    
    print("\n🎯 Pro Tips:")
    print("• Be specific with your tasks for better results")
    print("• Start with simple tasks and increase complexity gradually")
    print("• Use 'max_steps' parameter to limit agent actions")
    print("• Check the .env file to ensure your API key is set correctly")
    print("• Visit https://openrouter.ai/models to see available models")