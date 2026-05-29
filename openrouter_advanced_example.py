"""
Advanced example of using browser-use with OpenRouter API
This example shows more complex automation tasks with additional configuration.
"""

from browser_use import Agent, Browser, ChatOpenRouter
from browser_use.agent.views import AgentOutput
from dotenv import load_dotenv
import asyncio
import os
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

class NewsArticle(BaseModel):
    """Structured output model for news articles"""
    title: str = Field(description="Title of the news article")
    summary: str = Field(description="Brief summary of the article")
    source: str = Field(description="Source of the news article")
    date: str = Field(description="Publication date", default="Unknown")

async def advanced_news_search():
    """
    Advanced task: Search for news and extract structured data
    """
    # Using the direct ChatOpenRouter class for better OpenRouter integration
    llm = ChatOpenRouter(
        model='openai/gpt-4o-mini',  # You can change this to any OpenRouter model
        api_key=os.getenv('OPENROUTER_API_KEY'),
        temperature=0.1,
        # OpenRouter-specific parameter for tracking
        http_referer='https://your-app.com'  # Optional: your app's URL
    )
    
    # Create a more complex task
    task = """
        1. Go to https://news.google.com
        2. Search for 'artificial intelligence breakthroughs 2025'
        3. Extract the top 5 news articles with their titles, sources, and brief summaries
        4. Sort them by relevance
        """
    
    # Create a custom browser configuration
    browser = Browser(
        headless=False,  # Set to True to run without showing the browser window
        window_size={'width': 1200, 'height': 800},  # Browser window size
    )
    
    # Create the agent with structured output
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        max_steps=20,
        # Enable structured output to extract specific data
        output_model_schema=NewsArticle,
        use_vision=True,  # Enable vision for better page understanding
        vision_detail_level='low',  # 'low', 'high', or 'auto'
    )
    
    print(f"🚀 Starting advanced task: {task}")
    print(f"🤖 Using model: {llm.model} via OpenRouter")
    print(f"🌐 Browser: {'headless' if browser.config.headless else 'visible'}")
    
    # Run the agent and get the history
    history = await agent.run()
    
    print(f"✅ Task completed! Steps taken: {len(history.history)}")
    
    # Print structured output if available
    if history.structured_output:
        print(f"📋 Structured results:")
        for i, article in enumerate(history.structured_output, 1):
            print(f"  {i}. {article.title}")
            print(f"     Source: {article.source}")
            print(f"     Summary: {article.summary}")
            print()
    
    # Print final result if available
    if history.final_result():
        print(f"📝 Final result: {history.final_result()}")
    
    return history

async def e_commerce_task():
    """
    Example task: Search for products on an e-commerce site
    """
    llm = ChatOpenRouter(
        model='anthropic/claude-3-haiku',  # Using Claude Haiku as an example
        api_key=os.getenv('OPENROUTER_API_KEY'),
        temperature=0.1,
    )
    
    task = """
    1. Go to https://www.ecommerce-demo-site.com (or any e-commerce site)
    2. Search for 'wireless headphones'
    3. Find the top 3 products with the best ratings
    4. Extract their names, prices, and ratings
    5. Save the information to a file
    """
    
    agent = Agent(
        task=task,
        llm=llm,
        max_steps=25,
        use_vision=True,
    )
    
    print(f"🛒 Starting e-commerce task: Search for wireless headphones")
    print(f"🤖 Using model: {llm.model} via OpenRouter")
    
    history = await agent.run()
    
    print(f"✅ E-commerce task completed! Steps taken: {len(history.history)}")
    
    if history.final_result():
        print(f"📋 Results: {history.final_result()}")
    
    return history

if __name__ == "__main__":
    print("🌐 Browser-use with OpenRouter - Advanced Examples")
    print("=" * 55)
    
    # Make sure the API key is set
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        print("Please add your OpenRouter API key to the .env file")
        exit(1)
    
    print("Choose an example to run:")
    print("1. Advanced news search (structured output)")
    print("2. E-commerce product search")
    print("3. Run both")
    
    choice = input("Enter your choice (1/2/3): ").strip()
    
    if choice == "1":
        asyncio.run(advanced_news_search())
    elif choice == "2":
        asyncio.run(e_commerce_task())
    elif choice == "3":
        print("\n--- Running Advanced News Search ---")
        asyncio.run(advanced_news_search())
        print("\n--- Running E-commerce Task ---")
        asyncio.run(e_commerce_task())
    else:
        print("Invalid choice. Running advanced news search by default...")
        asyncio.run(advanced_news_search())