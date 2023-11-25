from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Users

from keyboards.vertical_reply_kb import make_vertical_reply_keyboard 

from data import WELCOME_MESSAGE, available_subscription_types, wait_message

from .states import MemberStates

from .functions import user_exists, can_generate_invite_link, generate_invite_link, get_sub_duration, is_admin

import asyncio

router = Router(name="main-router")

# ! /cancel
@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    await state.clear()
    await message.answer(
        "Your selections was canceled, please /start again to make new selections.",
        reply_markup=ReplyKeyboardRemove(),
    )

# ! /start
@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, state: FSMContext) -> None:
    
    # ? clear the state whenever user /start the bot
    await state.clear()
    if is_admin(str(message.from_user.id)):
        # ! Admin logic
        # TODO work in progress
        await message.answer(
            text="Hello, you are a admin!",
            reply_markup=ReplyKeyboardRemove())

        await state.set_state(MemberStates.admin_member) # ? set the state to admin_member
    
    else:
        # * Send a welcome message to everyone who starts the bot
        await message.answer(WELCOME_MESSAGE)
    
        if await user_exists(message.from_user.id, session, Users) == False:
            # ! New member logic
            
            await message.answer(
                text="Choose subscription type:",
                reply_markup=make_vertical_reply_keyboard(available_subscription_types))
            
            await state.set_state(MemberStates.new_member_choose_subscription_type) # ? set the state to new_member
        
        else:
            # ! Active member logic
            
            await message.answer(
                text="Hello, you are premium user! Type /status to see your subscription status. Type /join to receive invite link.",
                reply_markup=ReplyKeyboardRemove())
            
            await state.clear()


# ! /join
@router.message(Command("join"))
@router.message(F.text.casefold() == "join")
async def cmd_join(message: Message, session: AsyncSession, state: FSMContext, bot: Bot) -> None:
    
    # ? Generates invite link for the user to join premium group, sets the invite_link_generated to False

    await state.clear()
    # * Send a welcome message to everyone who starts the bot
    await message.answer(wait_message, reply_markup=ReplyKeyboardRemove())
    
    if await user_exists(message.from_user.id, session, Users) == True:
        
        if await can_generate_invite_link(message.from_user.id, session, Users) == True:
            invite_link = await generate_invite_link(message.from_user.id, session, Users, bot)
            invite_link_message = await message.answer(f"Invite link created: {invite_link}", reply_markup=ReplyKeyboardRemove())
            await asyncio.sleep(60)
            # delete the message after 1min
            await bot.delete_message(chat_id=invite_link_message.chat.id, message_id=invite_link_message.message_id)
            
            
        
        else:
            await message.answer("You already created an invite link, can only do that once! Type /status to see your subscription status.", reply_markup=ReplyKeyboardRemove())
            return
        
    else:
        
        await message.answer("You do not have active subscription! Please /start the bot to purchase one.", reply_markup=ReplyKeyboardRemove())
        return

# ! /status
@router.message(Command("status"))
@router.message(F.text.casefold() == "status")
async def cmd_status(message: Message, session: AsyncSession, state: FSMContext, bot: Bot) -> None:

    await state.clear()
    # * Send a welcome message to everyone who starts the bot
    await message.answer(wait_message, reply_markup=ReplyKeyboardRemove())

    if await user_exists(message.from_user.id, session, Users) == True:
        
        sub_duration = await get_sub_duration(message.from_user.id, session, Users)
        await message.answer(f"Your subscription will end in {sub_duration} days", reply_markup=make_vertical_reply_keyboard(["Cancel subscription"]))
        
        await state.set_state(MemberStates.active_member_cancel_subscription)
        
        
    else:
        
        await message.answer("You do not have active subscription! Please /start the bot to purchase one.", reply_markup=ReplyKeyboardRemove())
        return