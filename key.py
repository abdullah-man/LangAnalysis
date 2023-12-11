"""
This file contains code to save an api key in a .env file
and load it when needed
"""

import os
import sys

def save_api_key(key) -> bool:
    """
    Saves api key in a .env file in the parent directory
    """
    try:
        with open(".env", "w", encoding='utf-8') as file:
            file.write(f"OPENAI_API_KEY = {key}")
        return True
    except:
        return False

def read_api_key():
    pass
