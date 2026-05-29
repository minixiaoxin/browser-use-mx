# Using Browser-Use with OpenRouter API

This guide explains how to configure and run browser automation tasks using the browser-use library with OpenRouter API.

## Prerequisites

1. **OpenRouter API Key**: Get your API key from [OpenRouter](https://openrouter.ai/)
2. **Environment Setup**: Add your API key to the `.env` file:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

## Installation

Make sure you have the browser-use library installed with all dependencies:

```bash
# If you haven't already set up the environment
uv venv --python 3.11
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync
uvx browser-use install  # Install Chromium browser
```

## Basic Usage

### Method 1: Using ChatOpenAI with OpenRouter Base URL

```python
from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

llm = ChatOpenAI(
    model='openai/gpt-4o-mini',  # Any OpenRouter-compatible model
    base_url='https://openrouter.ai/api/v1',
    api_key=os.getenv('OPENROUTER_API_KEY'),
)

agent = Agent(
    task="Search for 'Python web scraping tutorial' and summarize results",
    llm=llm,
)

asyncio.run(agent.run())
```

### Method 2: Using ChatOpenRouter (Recommended)

```python
from browser_use import Agent
from browser_use.llm.openrouter.chat import ChatOpenRouter
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

llm = ChatOpenRouter(
    model='anthropic/claude-3-haiku',  # Any OpenRouter model
    api_key=os.getenv('OPENROUTER_API_KEY'),
    http_referer='https://your-app.com',  # Optional: for tracking
)

agent = Agent(
    task="Search for 'Python web scraping tutorial' and summarize results",
    llm=llm,
)

asyncio.run(agent.run())
```

## Available OpenRouter Models

You can use any model available on OpenRouter. Some popular options include:

- `openai/gpt-4o-mini` - Fast and capable
- `openai/gpt-4o` - More advanced reasoning
- `anthropic/claude-3-haiku` - Fast and efficient
- `anthropic/claude-3-sonnet` - Balanced performance
- `mistral/mistral-small` - Cost-effective
- `google/gemini-pro` - Google's powerful model

Visit [OpenRouter Models](https://openrouter.ai/models) to see all available models.

## Configuration Options

### Agent Configuration

```python
agent = Agent(
    task="Your specific task here",
    llm=llm,
    
    # Task execution limits
    max_steps=20,              # Maximum number of steps
    max_failures=5,            # Maximum failures before stopping
    llm_timeout=120,           # Timeout for LLM calls (seconds)
    step_timeout=180,          # Timeout for each step (seconds)
    
    # Vision and processing
    use_vision=True,           # Enable screenshot analysis
    vision_detail_level='low', # 'low', 'high', or 'auto'
    page_extraction_llm=None,  # Separate LLM for page content extraction
    
    # Behavior options
    use_thinking=True,         # Enable reasoning/thinking steps
    max_actions_per_step=3,    # Actions per step (e.g., for form filling)
    flash_mode=False,          # Fast mode (skips evaluation/reasoning)
    
    # Memory and history
    max_history_items=20,      # Number of history items to keep in context
    
    # Output options
    generate_gif=False,        # Generate GIF of automation
    save_conversation_path=None,  # Path to save conversation history
    
    # Browser (if not using default)
    browser=None,              # Custom browser instance
)
```

### Browser Configuration

```python
from browser_use import Browser

browser = Browser(
    headless=False,                    # Show browser window
    window_size={'width': 1200, 'height': 800},  # Window size
    keep_alive=True,                   # Keep browser alive after task
    allowed_domains=['example.com'],   # Restrict navigation to specific domains
    prohibited_domains=['bad-site.com'], # Block specific domains
    user_data_dir=None,                # Custom user data directory
    profile_directory='Default',       # Chrome profile to use
    proxy=None,                        # Proxy settings
    executable_path=None,              # Custom browser executable
    args=[],                          # Additional browser arguments
)
```

## Running Pre-built Examples

The repository includes several example scripts:

1. **Basic Example**:
   ```bash
   python openrouter_basic_example.py
   ```

2. **Advanced Example**:
   ```bash
   python openrouter_advanced_example.py
   ```

3. **Quick Start**:
   ```bash
   python run_openrouter_task.py
   ```

4. **Advanced Real-world Examples**:
   ```bash
   python advanced_openrouter_examples.py
   ```

## Common Task Examples

### Simple Search Task
```python
task = "Search for 'best AI tools 2025' on Google and summarize results"
```

### Data Extraction Task
```python
task = "Go to https://quotes.toscrape.com/ and extract the first 5 quotes with authors"
```

### Form Filling Task
```python
task = "Go to a job application site and fill out a sample application form"
```

### Structured Data Extraction
```python
from pydantic import BaseModel, Field

class NewsArticle(BaseModel):
    title: str = Field(description="Title of the news article")
    summary: str = Field(description="Brief summary of the article")
    source: str = Field(description="Source of the news article")

# Use with structured output
agent = Agent(
    task="Find latest AI news and extract structured information",
    llm=llm,
    output_model_schema=NewsArticle,  # Enables structured output
)
```

## Best Practices

1. **Be Specific**: Provide clear, detailed task descriptions
2. **Start Simple**: Begin with basic tasks before moving to complex ones
3. **Monitor Usage**: Keep track of your OpenRouter API usage
4. **Handle Errors**: Implement proper error handling for web automation
5. **Respect Websites**: Follow robots.txt and website terms of service
6. **Test Thoroughly**: Test tasks on different websites before production use

## Troubleshooting

- **API Key Issues**: Verify your OpenRouter API key in the `.env` file
- **Model Availability**: Check if the requested model is available on OpenRouter
- **Website Blocks**: Some sites may have anti-bot measures; try different approaches
- **Timeout Issues**: Increase timeout values for complex tasks
- **Rate Limits**: OpenRouter may have rate limits; adjust your usage accordingly

## Cost Management

- Monitor your OpenRouter usage through their dashboard
- Choose appropriate models based on task complexity
- Use `gpt-4o-mini` or `claude-3-haiku` for cost-effective operations
- Set appropriate `max_steps` to prevent infinite loops