"""
Basic test to verify browser-use installation
"""
import sys

# Test if we can import the main classes
try:
    from browser_use import Agent, Browser, ChatBrowserUse
    print("SUCCESS: Agent, Browser, and ChatBrowserUse classes imported successfully")
except ImportError as e:
    print(f"ERROR: Failed to import Agent/Browser/ChatBrowserUse: {e}")
    sys.exit(1)

# Test if browser views are available
try:
    from browser_use.browser.views import TabInfo, PageInfo
    print("SUCCESS: Browser views imported successfully")
except ImportError as e:
    print(f"ERROR: Failed to import browser views: {e}")
    sys.exit(1)

print("\nSUCCESS: All basic imports successful! The installation appears to be working correctly.")
print("\nTo run a full agent, you'll need to set up your API key in the .env file.")
print("See the AGENTS.md file for more information on supported models.")