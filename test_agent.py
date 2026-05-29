"""
Basic agent example to test the browser-use setup
"""
from browser_use import Agent, ChatBrowserUse
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

async def main():
    # Use ChatBrowserUse as recommended in AGENTS.md
    llm = ChatBrowserUse()
    task = "Find the number 1 post on Show HN"
    agent = Agent(task=task, llm=llm)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())