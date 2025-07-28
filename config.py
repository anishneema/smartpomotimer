import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for Focus Flow Agent"""
    
    # Nemotron API settings
    NEMOTRON_API_KEY = os.getenv("NEMOTRON_API_KEY", "")
    NEMOTRON_API_URL = os.getenv("NEMOTRON_API_URL", "https://api.nemotron.ai/v1/chat/completions")
    
    # Timer settings
    DEFAULT_FOCUS_DURATION = 25  # minutes
    DEFAULT_BREAK_DURATION = 5   # minutes
    
    # File paths
    LOG_FILE = "focus_flow_log.json"
    
    # Agent personality
    AGENT_NAME = "Focus Flow Agent"
    AGENT_VERSION = "MVP 1.0" 