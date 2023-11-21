from config import STRIPE_PRODUCT_1_ID, STRIPE_PRODUCT_2_ID, STRIPE_PRODUCT_3_ID

WELCOME_MESSAGE = """

CRYPTOJAB | PREMIUM
---
WELCOME TO CRYPTOJAB, YOUR PREMIUM GROUP FOR CRYPTO TRADING SIGNALS 🚀

🔔DAILY CRYPTO SIGNALS 🎓EDUCATIONAL CONTENT 📊IN-DEPTH MARKET ANALYSIS 📈TRADE STRATEGIES 🔔WEEKLY MARKET PREP CALL 💬PRIVATE Q&A ✅EXCLUSIVE PROMOS ✅EXCLUSIVE GIVEAWAYS ❗️LEARN AND EARN

In this group, you will receive only high-quality trading signals for cryptocurrencies. Long-term and short-term trades. We will also provide you with in-depth market analysis, trade strategies, and educational content to help you become a better trader.

Please note that all the content provided in the group is for educational purposes only and not as financial advice.

Remember, joining a Crypto Signals Telegram group can help you streamline your trading strategies, learn from experienced traders, and stay updated with the latest market news and trends cryptojab.com 🚀.
    
"""

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
        "button_text": "Coinbase (Crypto)",
    }
]

confirmation_messages = ["Confirm", "Cancel"]

available_subscription_types = [subscription["button_text"] for subscription in subscriptions]
available_subscription_types.append(confirmation_messages[1])

available_payment_methods = [payment["button_text"] for payment in payments]
available_payment_methods.append(confirmation_messages[1])