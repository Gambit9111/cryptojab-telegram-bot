from config import STRIPE_PRODUCT_1_ID, STRIPE_PRODUCT_2_ID, STRIPE_PRODUCT_3_ID, STRIPE_PRODUCT_4_ID, TELEGRAM_ADMIN_USERNAME

subscriptions = [
    {
        "id": 1,
        "price": 25,
        "duration": 30,
        "stripe_product_id": STRIPE_PRODUCT_1_ID,
        "button_text": "30 Days (25$)",
    },
    {
        "id": 2,
        "price": 180,
        "duration": 365,
        "stripe_product_id": STRIPE_PRODUCT_2_ID,
        "button_text": "365 Days (180$)",
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
WELCOME TO THE CRYPTOJAB PREMIUM EXPERIENCE WITH OUR ANALYSIS & INVESMENT IDEAS 🚀

🔔CRYPTO SIGNALS 🎓EDUCATIONAL CONTENT 📊IN-DEPTH MARKET ANALYSIS 📈TRADING STRATEGIES 🔔WEEKLY MARKET PREPARATION 💬PRIVATE Q&A ✅EXCLUSIVE PROMOS ✅EXCLUSIVE GIVEAWAYS ❗️LEARN AND EARN

In this group, you will not only receive high-quality trading signals for cryptocurrencies, but Long-term and short-term trades as well. We will also provide you with in-depth market analysis, trade strategies, and educational content to help you become a better trader overall.

Please note that all the content provided in the group is for educational purposes only and not should not be taken as financial advice.

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

# NEW MEMBER ROUTER ===>
CHOOSE_PAYMENT_METHOD_MESSAGE = "Choose your payment method:"

CRYPTO_PAYMENT_NOT_SUPPORTED_MESSAGE=f"Automated crypto payments are not supported yet, please contact administration if you wish to pay in cryptocurrencies {TELEGRAM_ADMIN_USERNAME}"
def SUBSCRIPTION_SELECTION_MESSAGE(subscription_type: str, payment_method: str) -> str:
    return f"You have chosen {subscription_type} with {payment_method} payment method"
CONFIRM_SELECTION_MESSAGE = "Please confirm your selection"
SELECTION_CONFIRMED_MESSAGE = "Selection confirmed, generating payment link..."
PAYMENT_MESSAGE = "Please click the button below to proceed to payment"
PAYMENT_BUTTON_MESSAGE = "Proceed to payment"
PAYMENT_BUTTON_DELETE_DURATION = 30 #SEC
AFTER_PAYMENT_JOIN_MESSAGE = "Type /join to get the invite link after your payment has been confirmed!"

#CANCEL SUB ROUTER ===>
CANCEL_SUBSCRIPTION_BUTTON_MESSAGE = "Cancel subscription"
CANCEL_SUBSCRIPTION_CONFIRMATION_MESSAGE = "Are you sure you want to cancel your subscription? You will be kicked out of the group and will not be able to join before you purchase again."
SUBSCRIPTION_CANCELED_MESSAGE = "Your subscription has been cancelled. Thank your for using our services!"
SUBSCRIPTION_NOT_CANCELED_MESSAGE = "Your subscription has not been cancelled."

#ADMIN ROUTER ===> 
ADD_MEMBER_MESSAGE = "Enter the Telegram ID of the new member, Enter duration of days. In a format like this: telegram_id,days --> 12837927,90"
KICK_MEMBER_MESSAGE = "Enter the Telegram ID of the member you want to kick"
WRONG_FORMAT_MESSAGE = "Wrong format. Please try again"
ADDING_MEMBER_MESSAGE = "Adding member, please wait..."
ADDING_MEMBER_SUCCESS_MESSAGE = "Member added successfully!"
KICKING_MEMBER_MESSSAGE = "Kicking member, please wait..."
KICKING_MEMBER_SUCCESS_MESSAGE = "Member kicked successfully!"

#CATCH ALL ROUTER ===>
CATCH_ALL_MESSAGE = "Please /start the bot to use it"
CATCH_ALL_WRONG_TYPE_MESSAGE = "You can only send messages to this bot"

def UNKNOWN_COMMAND_ERROR_MESSAGE_DISPLAY(error: str) -> str:
    return f"Unknown Command. {error}"

UNKNOWN_COMMAND_ERROR_MESSAGES=["Please choose one of the available subscription types",
                                "Please choose one of the available payment methods",
                                "Please choose one of the available confirmation messages",
                                "Please choose one of the available commands"]

confirmation_messages = ["Confirm", "Cancel"]
admin_options = ["Add member", "Kick member"]
cancel_subscription_confirmation_messages = ["Yes, cancel my subscription", "No, keep my subscription"]

available_subscription_types = [subscription["button_text"] for subscription in subscriptions]
available_subscription_types.append(confirmation_messages[1])

available_payment_methods = [payment["button_text"] for payment in payments]
available_payment_methods.append(confirmation_messages[1])
