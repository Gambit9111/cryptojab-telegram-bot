from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
import asyncio


from aiogram.fsm.context import FSMContext

from keyboards.vertical_reply_kb import make_vertical_reply_keyboard 

from data import available_subscription_types, available_payment_methods, confirmation_messages

from .states import MemberStates

from .checkout import create_checkout_session



router = Router(name="new-member-router")

# * 1)
# ! will run after NEW MEMBER chooses his subscription type
@router.message(MemberStates.new_member_choose_subscription_type, F.text.in_(available_subscription_types))
async def subscription_type_choosen(message: Message, state: FSMContext):
    await state.update_data(subscription_type=message.text)
    
    await message.answer(
        text="Choose your payment method:",
        reply_markup=make_vertical_reply_keyboard(available_payment_methods))
    await state.set_state(MemberStates.new_member_choose_payment_method)

# ? will run if NEW MEMBER choose a subscription type that does not exist
@router.message(MemberStates.new_member_choose_subscription_type)
async def wrong_subscription_type_choosen(message: Message):
    await message.answer(text="Unknown Command. Please choose one of the available subscription types", reply_markup=make_vertical_reply_keyboard(available_subscription_types))


# * 2)
# ! will run after NEW MEMBER chooses his payment method
@router.message(MemberStates.new_member_choose_payment_method, F.text.in_(available_payment_methods))
async def payment_method_choosen(message: Message, state: FSMContext):
    await state.update_data(payment_method=message.text)
    
    # get the subscription type and payment method from state
    state_data = await state.get_data()
    subscription_type = state_data.get("subscription_type")
    payment_method = state_data.get("payment_method")

    if payment_method == "Coinbase (Crypto)":
        await message.answer(text="Automated crypto payments are not supported yet, please contact administration if you wish to pay in cryptocurrencies...", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        # send user a message with his subscription type and payment method
        await message.answer(text=f"You have chosen {subscription_type} with {payment_method} payment method")
        
        await message.answer(text="Please confirm your selection", reply_markup=make_vertical_reply_keyboard(confirmation_messages))
        await state.set_state(MemberStates.new_member_generate_payment_link)

# ? will run if NEW MEMBER choose a payment method that does not exist
@router.message(MemberStates.new_member_choose_payment_method)
async def wrong_payment_method_choosen(message: Message):
    await message.answer(text="Unknown Command. Please choose one of the available payment methods", reply_markup=make_vertical_reply_keyboard(available_payment_methods))


# * 3)
# ! will run after NEW MEMBER confirms his payment
@router.message(MemberStates.new_member_generate_payment_link, F.text.in_(confirmation_messages))
async def confirm_payment(message: Message, state: FSMContext, bot: Bot):
    
    # get the subscription type and payment method from state
    state_data = await state.get_data()
    subscription_type = state_data.get("subscription_type")
    payment_method = state_data.get("payment_method")
        
    await message.answer(text="Selection confirmed, generating payment link...", reply_markup=ReplyKeyboardRemove())
    checkout_url = await create_checkout_session(message.from_user.id, subscription_type, payment_method)
    checkout_message = await message.answer(text=f"Checkout url {checkout_url}")
    await state.clear()

    # delete the checkout url after 1min
    await asyncio.sleep(60)
    await bot.delete_message(chat_id=checkout_message.chat.id, message_id=checkout_message.message_id)
    await message.answer(text="Type /join to get the invite link after your payment has been confirmed!", reply_markup=ReplyKeyboardRemove())

# ? will run if NEW MEMBER choose a confirmation message that does not exist
@router.message(MemberStates.new_member_generate_payment_link)
async def confirm_payment(message: Message, state: FSMContext):
    await message.answer(text="Unknown Command. Please choose one of the available confirmation messages", reply_markup=make_vertical_reply_keyboard(confirmation_messages))