import stripe
# from coinbase_commerce.client import Client

from data import subscriptions, payments
from config import STRIPE_API_KEY, STRIPE_CHECKOUT_SUCCESS_URL, STRIPE_CHECKOUT_CANCEL_URL #, COINBASE_API_KEY

stripe.api_key = STRIPE_API_KEY

# coinbase_base_url = "https://commerce.coinbase.com/checkout/"
# coinbase_client = Client(api_key=COINBASE_API_KEY)

async def create_checkout_session(telegram_id: int, subscription_type: str, payment_method: str) -> str:
    """creates new checkout session for the user
    Args:
        telegram_id (int): _description_
        subscription_type (str): _description_
        payment_method (str): _description_

    Returns:
        str: returns URL of the checkout session
    """
    # Find the subscription that matches the subscription_type
    matching_subscriptions = [sub for sub in subscriptions if sub["button_text"] == subscription_type]
    matching_payments = [pay for pay in payments if pay["button_text"] == payment_method]

    # If no matching subscription was found, return an error message
    if not matching_subscriptions or not matching_payments:
        raise ValueError("Please check your data.py file, there is no subscription or payment with this button_text")

    # If multiple matching subscriptions were found, return an error message
    if len(matching_subscriptions) > 1 or len(matching_payments) > 1:
        raise ValueError("Please check your data.py file, there are multiple subscriptions or payments with this button_text")

    # If exactly one matching subscription and payment was found, extract the data
    matching_subscription = matching_subscriptions[0]
    matching_payment = matching_payments[0]
    
    # ? needed stuff
    price = matching_subscription["price"]
    duration = matching_subscription["duration"]
    stripe_product_id = matching_subscription["stripe_product_id"]
    payment_method = matching_payment["name"]
    
    # ? stripe checkout session
    if payment_method == "Stripe":
        print("creating checkout session", telegram_id + price, duration, stripe_product_id, payment_method)
        
        stripe_checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': stripe_product_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=STRIPE_CHECKOUT_SUCCESS_URL,
            cancel_url=STRIPE_CHECKOUT_CANCEL_URL,
            metadata={'telegram_id': telegram_id, 'duration': duration},
            subscription_data={
                'metadata': {
                    'telegram_id': telegram_id,
                    'duration': duration,
                }
            }
        )
        
        return stripe_checkout_session["url"] # ? return the URL of the checkout session
    
    # ? coinbase checkout session
    # elif payment_method == "Coinbase":
    #     print("creating checkout session", telegram_id + price, duration, stripe_product_id, payment_method)

    #     coinbase_checkout_info = {
    #         "name": f"Subscription for {duration} days",
    #         "description": telegram_id,
    #         "local_price": {
    #             "amount": 0.1,
    #             "currency": "USD"
    #         },
    #         "pricing_type": "fixed_price",
    #         "requested_info": ["email"]
    #     }
        
    #     coinbase_checkout_session = coinbase_client.checkout.create(**coinbase_checkout_info)
        
    #     return coinbase_base_url + coinbase_checkout_session["id"] # ? return the URL of the checkout session
    
    else:
        raise ValueError("Plese check your data.py file, something aint right with the payment_method")