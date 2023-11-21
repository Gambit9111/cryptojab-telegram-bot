from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from db.models import User

from .functions import user_exists

from .data import WELCOME_MESSAGE, available_subscription_types, available_payment_methods, confirmation_messages

from keyboards.vertical_reply_kb import make_vertical_reply_keyboard 

router = Router(name="main-router")

isAdmin = False

class MemberStates(StatesGroup):
    
    admin_member = State()
    
    new_member_choose_subscription_type = State()
    new_member_choose_payment_method = State()
    new_member_generate_payment_link = State()
    
    active_member_get_invite_link = State()
    active_member_view_sub_info = State()
    active_member_cancel_subscription = State()


# ! /cancel
@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Your selections was canceled, please /start again to make new selections.",
        reply_markup=ReplyKeyboardRemove(),
    )

# ! /start
@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, state: FSMContext):
    
    # ? clear the state whenever user /start the bot
    await state.clear()
    # * Send a welcome message to everyone who starts the bot
    await message.answer(WELCOME_MESSAGE, reply_markup=ReplyKeyboardRemove())
    
    if isAdmin:
        # ! Admin logic
        # TODO work in progress
        await message.answer(
            text="Hello, you are a admin!",
            reply_markup=ReplyKeyboardRemove())

        await state.set_state(MemberStates.admin_member) # ? set the state to admin_member
    
    elif await user_exists(message.from_user.id, session, User) == False:
        # ! New member logic
        
        await message.answer(
            text="Choose subscription type:",
            reply_markup=make_vertical_reply_keyboard(available_subscription_types))
        
        await state.set_state(MemberStates.new_member_choose_subscription_type) # ? set the state to new_member
        
    
    else:
        # ! Active member logic
        
        await message.answer(
            text="Hello, you are a active user!",
            reply_markup=ReplyKeyboardRemove())
        
        await state.set_state(MemberStates.active_member_view_sub_info) # ? set the state to active_member


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