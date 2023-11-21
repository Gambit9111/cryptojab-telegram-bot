from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User

from keyboards.vertical_reply_kb import make_vertical_reply_keyboard 

from data import WELCOME_MESSAGE, available_subscription_types

from .states import MemberStates

from .functions import user_exists

router = Router(name="main-router")

isAdmin = False

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
