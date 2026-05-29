"""
Advanced real-world automation examples using OpenRouter with browser-use
"""

from browser_use import Agent, Browser, ChatOpenRouter
from browser_use.agent.views import AgentOutput
from dotenv import load_dotenv
import asyncio
import os
from pydantic import BaseModel, Field
import json

load_dotenv()

class JobPosting(BaseModel):
    """Model for extracting job posting information"""
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    location: str = Field(description="Job location")
    salary: str = Field(description="Salary range if mentioned")
    description: str = Field(description="Brief job description")
    posted_date: str = Field(description="When the job was posted")

class ProductInfo(BaseModel):
    """Model for extracting product information"""
    name: str = Field(description="Product name")
    price: str = Field(description="Product price")
    rating: float = Field(description="Product rating out of 5")
    review_count: int = Field(description="Number of reviews")
    description: str = Field(description="Product description")

async def job_search_automation():
    """Example: Automated job search and extraction"""
    print("🔍 Starting Job Search Automation...")
    
    llm = ChatOpenRouter(
        model='openai/gpt-4o-mini',
        api_key=os.getenv('OPENROUTER_API_KEY'),
        temperature=0.1,
    )
    
    task = """
    1. Go to LinkedIn Jobs or Indeed
    2. Search for 'remote Python developer' jobs
    3. Extract information for the top 5 job postings:
       - Job title
       - Company name
       - Location
       - Salary (if mentioned)
       - Brief description
       - When posted
    4. Return the information in a structured format
    """
    
    agent = Agent(
        task=task,
        llm=llm,
        max_steps=25,
        output_model_schema=JobPosting,
        use_vision=True,
        vision_detail_level='low',
    )
    
    history = await agent.run()
    
    if history.structured_output:
        print("📋 Found Job Postings:")
        for i, job in enumerate(history.structured_output, 1):
            print(f"\n{i}. {job.title}")
            print(f"   Company: {job.company}")
            print(f"   Location: {job.location}")
            print(f"   Salary: {job.salary}")
            print(f"   Posted: {job.posted_date}")
            print(f"   Description: {job.description[:100]}...")
    
    return history

async def product_comparison_automation():
    """Example: Automated product comparison"""
    print("🛒 Starting Product Comparison Automation...")
    
    llm = ChatOpenRouter(
        model='anthropic/claude-3-haiku',
        api_key=os.getenv('OPENROUTER_API_KEY'),
        temperature=0.1,
    )
    
    task = """
    1. Go to Amazon or another e-commerce site
    2. Search for 'wireless earbuds'
    3. Find and compare the top 3 products:
       - Product name
       - Price
       - Customer rating
       - Number of reviews
       - Brief description
    4. Present the comparison in a structured format
    """
    
    agent = Agent(
        task=task,
        llm=llm,
        max_steps=30,
        output_model_schema=ProductInfo,
        use_vision=True,
        vision_detail_level='low',
    )
    
    history = await agent.run()
    
    if history.structured_output:
        print("📋 Product Comparison Results:")
        for i, product in enumerate(history.structured_output, 1):
            print(f"\n{i}. {product.name}")
            print(f"   Price: {product.price}")
            print(f"   Rating: {product.rating}/5 ({product.review_count} reviews)")
            print(f"   Description: {product.description[:100]}...")
    
    return history

async def news_analysis_automation():
    """Example: Automated news analysis and summarization"""
    print("📰 Starting News Analysis Automation...")
    
    llm = ChatOpenRouter(
        model='openai/gpt-4o',
        api_key=os.getenv('OPENROUTER_API_KEY'),
        temperature=0.2,
    )
    
    task = """
    1. Go to a major news site like BBC, CNN, or Reuters
    2. Find the latest news about artificial intelligence
    3. Extract the top 5 AI-related news stories with:
       - Headline
       - Source
       - Brief summary
       - Publication date
       - Key points mentioned
    4. Summarize the overall AI news landscape from these articles
    """
    
    agent = Agent(
        task=task,
        llm=llm,
        max_steps=20,
        use_vision=True,
        max_actions_per_step=2,  # Allow multiple actions per step for efficiency
    )
    
    history = await agent.run()
    
    print("📋 News Analysis Results:")
    if history.final_result():
        print(history.final_result())
    
    return history

async def social_media_monitoring():
    """Example: Social media monitoring (for demonstration - respecting robots.txt)"""
    print("📊 Starting Social Media Monitoring Simulation...")
    
    llm = ChatOpenRouter(
        model='mistral/mistral-small',
        api_key=os.getenv('OPENROUTER_API_KEY'),
        temperature=0.3,
    )
    
    task = """
    1. Go to a public forum or news site that discusses technology
    2. Search for discussions about 'new AI tools' or 'AI developments'
    3. Extract the top 5 recent discussions with:
       - Topic/title of discussion
       - Main points mentioned
       - General sentiment (positive, negative, neutral)
       - Key concerns or excitement mentioned
    """
    
    agent = Agent(
        task=task,
        llm=llm,
        max_steps=25,
        use_vision=True,
    )
    
    history = await agent.run()
    
    print("📋 Social Media Monitoring Results:")
    if history.final_result():
        print(history.final_result())
    
    return history

async def run_all_examples():
    """Run all advanced examples (comment out the ones you don't want to run)"""
    print("🚀 Running Advanced Automation Examples with OpenRouter")
    print("=" * 60)
    
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        return
    
    examples = [
        ("Job Search", job_search_automation),
        ("Product Comparison", product_comparison_automation),
        ("News Analysis", news_analysis_automation),
        ("Social Media Monitoring", social_media_monitoring),
    ]
    
    for name, func in examples:
        print(f"\n{'='*20} {name} Example {'='*20}")
        try:
            await func()
            print(f"\n✅ {name} example completed successfully!")
        except Exception as e:
            print(f"\n⚠️ {name} example encountered an error: {str(e)}")
            print("This is normal for web automation as sites change frequently")
        
        # Ask if user wants to continue
        continue_prompt = input("\nContinue to next example? (y/n): ").strip().lower()
        if continue_prompt != 'y':
            break

if __name__ == "__main__":
    print("Advanced Browser Automation Examples with OpenRouter")
    print("=" * 55)
    
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        print("Please add your OpenRouter API key to the .env file")
        exit(1)
    
    print("Available Examples:")
    print("1. Job Search Automation")
    print("2. Product Comparison Automation") 
    print("3. News Analysis Automation")
    print("4. Social Media Monitoring")
    print("5. Run All Examples")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        asyncio.run(job_search_automation())
    elif choice == "2":
        asyncio.run(product_comparison_automation())
    elif choice == "3":
        asyncio.run(news_analysis_automation())
    elif choice == "4":
        asyncio.run(social_media_monitoring())
    elif choice == "5":
        asyncio.run(run_all_examples())
    else:
        print("Invalid choice. Running job search automation as default...")
        asyncio.run(job_search_automation())
    
    print("\n🎯 Tips for Success:")
    print("• Always be specific with your task descriptions")
    print("• Start with simple tasks before moving to complex ones")
    print("• Monitor the agent's progress and adjust max_steps as needed")
    print("• Check that target websites allow automated access")
    print("• Some websites may have anti-bot measures")