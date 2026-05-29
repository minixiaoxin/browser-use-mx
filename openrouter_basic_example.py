'''
Author: GZQ
Date: 2025-12-25 11:13:28
LastEditTime: 2025-12-25 14:17:54
LastEditors: GZQ
version: 
Description: 
FilePath: \browser-use-0.11.2\openrouter_basic_example.py
'''
"""
Basic example of using browser-use with OpenRouter API
This example shows how to set up and run a simple automation task.
"""

from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv
import asyncio
import os

# Load environment variables from .env file
load_dotenv()

async def basic_search_task():
    """
    Basic task: Search for information on the web
    """
    # Configure the LLM to use OpenRouter
    llm = ChatOpenAI(
        model='openai/gpt-4o-mini',  # Using GPT-4o-mini as an example
        base_url='https://openrouter.ai/api/v1',
        api_key=os.getenv('OPENROUTER_API_KEY'),
        temperature=0.1,
    )
    
    # Create the agent with a specific task
    task = "Search for the latest news about artificial intelligence on Google and summarize the top 3 results"
    
    agent = Agent(
        task=task,
        llm=llm,
        # Optional: configure additional settings
        max_steps=15,  # Maximum number of steps the agent can take
        use_vision=False,  # Set to True if you want to enable screenshots
    )
    
    print(f"🚀 Starting task: {task}")
    print(f"🤖 Using model: {llm.model} via OpenRouter")
    
    # Run the agent and get the history
    history = await agent.run()
    
    print(f"✅ Task completed! Steps taken: {len(history.history)}")
    
    # Print the final result if available
    if history.final_result():
        print(f"📋 Final result: {history.final_result()}")
    
    return history

if __name__ == "__main__":
    print("🌐 Browser-use with OpenRouter - Basic Example")
    print("=" * 50)
    
    # Make sure the API key is set
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        print("Please add your OpenRouter API key to the .env file")
        exit(1)
    
    asyncio.run(basic_search_task())