from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.context import FSMContext

from keyboards.vertical_reply_kb import make_vertical_reply_keyboard 

from data import available_subscription_types, available_payment_methods, confirmation_messages

from .states import MemberStates


router = Router(name="new-member-router")

# ! will run after NEW MEMBER chooses his subscription type
@router.message(MemberStates.new_member_choose_subscription_type, F.text.in_(available_subscription_types))
async def subscription_type_choosen(message: Message, state: FSMContext):
    await state.update_data(subscription_type=message.text)
    await message.answer(
        text="Choose your payment method:",
        reply_markup=make_vertical_reply_keyboard(available_payment_methods))
    await state.set_state(MemberStates.new_member_choose_payment_method)

# ! will run if NEW MEMBER choose a subscription type that does not exist
@router.message(MemberStates.new_member_choose_subscription_type)
async def wrong_subscription_type_choosen(message: Message):
    await message.answer(text="Please choose one of the available subscription types", reply_markup=make_vertical_reply_keyboard(available_subscription_types))

# ! will run after NEW MEMBER chooses his payment method
@router.message(MemberStates.new_member_choose_payment_method, F.text.in_(available_payment_methods))
async def payment_method_choosen(message: Message, state: FSMContext):
    await state.update_data(payment_method=message.text)
    await message.answer(text="Please confirm your payment", reply_markup=make_vertical_reply_keyboard(confirmation_messages))
    await state.set_state(MemberStates.new_member_generate_payment_link)

# ! will run if NEW MEMBER choose a payment method that does not exist
@router.message(MemberStates.new_member_choose_payment_method)
async def wrong_payment_method_choosen(message: Message):
    await message.answer(text="Please choose one of the available payment methods", reply_markup=make_vertical_reply_keyboard(available_payment_methods))

# ! will run after NEW MEMBER confirms his payment
@router.message(MemberStates.new_member_generate_payment_link, F.text.in_(confirmation_messages))
async def confirm_payment(message: Message, state: FSMContext):
    await message.answer(text="Payment confirmed, generating payment link...", reply_markup=ReplyKeyboardRemove())
    await state.clear()