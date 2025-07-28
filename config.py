import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for Focus Flow Agent"""
    
    # Nemotron API settings (NVIDIA API)
    NEMOTRON_API_KEY = os.getenv("NEMOTRON_API_KEY", "")
    NEMOTRON_API_URL = os.getenv("NEMOTRON_API_URL", "https://integrate.api.nvidia.com/v1")
    NEMOTRON_MODEL = os.getenv("NEMOTRON_MODEL", "nvidia/llama-3.3-nemotron-super-49b-v1.5")
    
    # Timer settings
    DEFAULT_FOCUS_DURATION = 25  # minutes
    DEFAULT_BREAK_DURATION = 5   # minutes
    
    # File paths
    LOG_FILE = "focus_flow_log.json"
    
    # Agent personality
    AGENT_NAME = "Focus Flow Agent"
    AGENT_VERSION = "MVP 1.0" 