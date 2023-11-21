import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DB_URL = os.getenv("DB_URL")
TELEGRAM_WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")
TELEGRAM_ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID")
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
WEB_SERVER_PORT = os.getenv("WEB_SERVER_PORT")
STRIPE_PRODUCT_1_ID = os.getenv("STRIPE_PRODUCT_1_ID")
STRIPE_PRODUCT_2_ID = os.getenv("STRIPE_PRODUCT_2_ID")
STRIPE_PRODUCT_3_ID = os.getenv("STRIPE_PRODUCT_3_ID")

if TELEGRAM_BOT_TOKEN is None:
    raise ValueError("Please set TELEGRAM_BOT_TOKEN environment variable")
if DB_URL is None:    
    raise ValueError("Please set DB_URL environment variable")
if TELEGRAM_WEBHOOK_URL is None:
    raise ValueError("Please set TELEGRAM_WEBHOOK_URL environment variable")
if TELEGRAM_WEBHOOK_SECRET is None:
    raise ValueError("Please set TELEGRAM_WEBHOOK_SECRET environment variable")
if TELEGRAM_ADMIN_ID is None:
    raise ValueError("Please set TELEGRAM_ADMIN_ID environment variable")
if WEB_SERVER_HOST is None:
    raise ValueError("Please set WEB_SERVER_HOST environment variable")
if WEB_SERVER_PORT is None:
    raise ValueError("Please set WEB_SERVER_PORT environment variable")
if STRIPE_PRODUCT_1_ID is None:
    raise ValueError("Please set STRIPE_PRODUCT_1_ID environment variable")
if STRIPE_PRODUCT_2_ID is None:
    raise ValueError("Please set STRIPE_PRODUCT_2_ID environment variable")
if STRIPE_PRODUCT_3_ID is None:
    raise ValueError("Please set STRIPE_PRODUCT_3_ID environment variable")
else:
    print("Environment variables are set")