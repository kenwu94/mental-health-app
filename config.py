import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Store your configuration settings here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Get API key from environment variable
DEFAULT_ALARM_TIME = "09:00"
USER_DATA_FILE = "data/user_data.json"

# Validate API key is available
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not found in environment variables.")
    print("Please create a .env file with your API key or set it as an environment variable.")