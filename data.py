from config import STRIPE_PRODUCT_1_ID, STRIPE_PRODUCT_2_ID, STRIPE_PRODUCT_3_ID, STRIPE_PRODUCT_4_ID, TELEGRAM_ADMIN_USERNAME

subscriptions = [
    {
        "id": 1,
        "price": 45,
        "duration": 30,
        "stripe_product_id": STRIPE_PRODUCT_1_ID,
        "button_text": "30 Days (45$)",
    },
    {
        "id": 2,
        "price": 120,
        "duration": 90,
        "stripe_product_id": STRIPE_PRODUCT_2_ID,
        "button_text": "90 Days (120$)",
    },
    {
        "id": 3,
        "price": 365,
        "duration": 365,
        "stripe_product_id": STRIPE_PRODUCT_3_ID,
        "button_text": "365 Days (365$)",
    },
    {
        "id": 4,
        "price": 15,
        "duration": 1,
        "stripe_product_id": STRIPE_PRODUCT_4_ID,
        "button_text": "1 Days (15$)",
    },
]

payments = [
    {
        "id": 1,
        "name": "Stripe",
        "button_text": "Stripe (Credit Card)",
    },
    {
        "id": 2,
        "name": "Coinbase",
        "button_text": "Crypto",
    }
]

WELCOME_MESSAGE = """

CRYPTOJAB | PREMIUM
---
WELCOME TO CRYPTOJAB, YOUR PREMIUM GROUP FOR CRYPTO TRADING SIGNALS 🚀

🔔DAILY CRYPTO SIGNALS 🎓EDUCATIONAL CONTENT 📊IN-DEPTH MARKET ANALYSIS 📈TRADE STRATEGIES 🔔WEEKLY MARKET PREP CALL 💬PRIVATE Q&A ✅EXCLUSIVE PROMOS ✅EXCLUSIVE GIVEAWAYS ❗️LEARN AND EARN

In this group, you will receive only high-quality trading signals for cryptocurrencies. Long-term and short-term trades. We will also provide you with in-depth market analysis, trade strategies, and educational content to help you become a better trader.

Please note that all the content provided in the group is for educational purposes only and not as financial advice.

Remember, joining a Crypto Signals Telegram group can help you streamline your trading strategies, learn from experienced traders, and stay updated with the latest market news and trends cryptojab.com 🚀.
    
"""
# MAIN ROUTER ===>
CANCEL_SELECTION_MESSAGE = "Your selections was canceled, please /start again to make new selections."
ADMIN_MODE_START_MESSAGE = "Hello Admin! Choose your action."
CHOOSE_SUBSCRIPTION_TYPE_MESSAGE = "Please select your subscription type:"
PREMIUM_USER_START_MESSAGE = "Hello, you are premium user! Type /status to see your subscription status. Type /join to receive invite link."
CHANNEL_INVITE_MESSAGE = "Click the button to join."
CHANNEL_INVITE_BUTTON_MESSAGE = "Join"
INVITE_LINK_ALREADY_CREATED_MESSAGE = "You already created an invite link, can only do that once! Type /status to see your subscription status."
def SUB_DURATION_MESSAGE(sub_duration: int) -> str:
    return f"Your subscription will end in {sub_duration} days"
NO_ACTIVE_SUBSCRIPTION_MESSAGE = "You do not have active subscription! Please /start the bot to purchase one."
HELP_COMMAND_MESSAGE = f"If you have any questions or wish to pay with crypto, please contact our support team: {TELEGRAM_ADMIN_USERNAME}"
WAIT_MESSAGE = "Checking status of your account. Please wait..."


confirmation_messages = ["Confirm", "Cancel"]
admin_options = ["Add member", "Kick member"]
cancel_subscription_confirmation_messages = ["Yes, cancel my subscription", "No, keep my subscription"]

available_subscription_types = [subscription["button_text"] for subscription in subscriptions]
available_subscription_types.append(confirmation_messages[1])

available_payment_methods = [payment["button_text"] for payment in payments]
available_payment_methods.append(confirmation_messages[1])