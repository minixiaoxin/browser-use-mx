"""
Configuration Guide: Using browser-use with OpenRouter API

This guide explains how to configure and run browser automation tasks 
using OpenRouter API with various models.
"""

# 1. Environment Setup
# Make sure your .env file contains:
"""
OPENROUTER_API_KEY=your_openrouter_api_key_here
"""

# 2. Basic Configuration Options
from browser_use import Agent, ChatOpenRouter, Browser
from dotenv import load_dotenv
import os

load_dotenv()

# Different ways to configure the LLM
def configure_llm_examples():
    # Method 1: Using ChatOpenAI with OpenRouter base URL
    from browser_use import ChatOpenAI
    llm1 = ChatOpenAI(
        model='openai/gpt-4o-mini',
        base_url='https://openrouter.ai/api/v1',
        api_key=os.getenv('OPENROUTER_API_KEY'),
    )
    
    # Method 2: Using ChatOpenRouter (recommended for OpenRouter)
    llm2 = ChatOpenRouter(
        model='anthropic/claude-3-haiku',
        api_key=os.getenv('OPENROUTER_API_KEY'),
        http_referer='https://your-app.com',  # Optional: for tracking
    )
    
    return llm1, llm2

# 3. Browser Configuration Options
def configure_browser_examples():
    # Basic browser setup
    browser_basic = Browser(headless=False)
    
    # Advanced browser setup
    browser_advanced = Browser(
        headless=False,  # Set to True for headless operation
        window_size={'width': 1400, 'height': 900},
        viewport={'width': 1400, 'height': 900},
        keep_alive=True,  # Keep browser alive after task completion
        allowed_domains=['example.com', '*.google.com'],  # Restrict navigation
    )
    
    return browser_basic, browser_advanced

# 4. Agent Configuration Options
def configure_agent_examples():
    llm = ChatOpenRouter(
        model='openai/gpt-4o-mini',
        api_key=os.getenv('OPENROUTER_API_KEY'),
    )
    
    # Basic agent
    agent_basic = Agent(
        task="Search for Python tutorials",
        llm=llm,
    )
    
    # Advanced agent with many options
    agent_advanced = Agent(
        task="Find the best Python web scraping tutorials from 2025",
        llm=llm,
        max_steps=30,  # Maximum steps before stopping
        max_failures=5,  # Maximum failures before stopping
        use_vision=True,  # Enable screenshot analysis
        vision_detail_level='auto',  # 'low', 'high', or 'auto'
        use_thinking=True,  # Enable reasoning/thinking steps
        max_history_items=20,  # Number of history items to keep in context
        llm_timeout=120,  # Timeout for LLM calls in seconds
        step_timeout=180,  # Timeout for each step in seconds
        generate_gif=True,  # Generate GIF of the automation (optional)
    )
    
    return agent_basic, agent_advanced

# 5. Common Task Examples
async def run_common_tasks():
    llm = ChatOpenRouter(
        model='openai/gpt-4o-mini',
        api_key=os.getenv('OPENROUTER_API_KEY'),
    )
    
    # Task 1: Simple search
    search_agent = Agent(
        task="Search for 'best AI tools 2025' on Google and summarize results",
        llm=llm,
        max_steps=15
    )
    await search_agent.run()
    
    # Task 2: Data extraction
    extraction_agent = Agent(
        task="Go to https://quotes.toscrape.com/ and extract the first 5 quotes with authors",
        llm=llm,
        max_steps=10
    )
    await extraction_agent.run()
    
    # Task 3: Form filling
    form_agent = Agent(
        task="Go to a job application site and fill out a sample application form",
        llm=llm,
        max_steps=20
    )
    await form_agent.run()

# 6. Error Handling and Best Practices
async def robust_task_execution():
    llm = ChatOpenRouter(
        model='openai/gpt-4o-mini',
        api_key=os.getenv('OPENROUTER_API_KEY'),
    )
    
    task = "Perform a complex web automation task"
    
    try:
        agent = Agent(
            task=task,
            llm=llm,
            max_steps=50,
            max_failures=10,
            use_vision=True,
        )
        
        history = await agent.run()
        
        # Check if the task was successful
        if history.is_successful():
            print("✅ Task completed successfully!")
            print(f"Final result: {history.final_result()}")
        else:
            print("⚠️ Task completed but may not have achieved the goal")
            print(f"Final state: {history.final_result()}")
            
    except Exception as e:
        print(f"❌ Error during task execution: {str(e)}")
        
        # The agent might have partial results even if there was an error
        if 'history' in locals():
            print(f"Partial results: {history.final_result()}")

# 7. Running the Examples
if __name__ == "__main__":
    print("Browser-use with OpenRouter Configuration Guide")
    print("=" * 50)
    
    # Check if API key is available
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        print("Please add your OpenRouter API key to the .env file")
        exit(1)
    
    print("✅ OpenRouter API key found")
    print("Configuration examples loaded successfully!")
    print("\nYou can now run your automation tasks using the examples above.")