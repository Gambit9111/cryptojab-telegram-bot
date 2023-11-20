import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DB_URL = os.getenv("DB_URL")

if TELEGRAM_BOT_TOKEN is None:
    raise ValueError("Please set TELEGRAM_BOT_TOKEN environment variable")
if DB_URL is None:    
    raise ValueError("Please set DB_URL environment variable")
else:
    print("Environment variables are set")