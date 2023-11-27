from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Users

from keyboards.vertical_reply_kb import make_vertical_reply_keyboard 
from keyboards.link_button import make_link_button

from data import (WELCOME_MESSAGE,
                  CANCEL_SELECTION_MESSAGE,
                  ADMIN_MODE_START_MESSAGE,
                  CHOOSE_SUBSCRIPTION_TYPE_MESSAGE,
                  PREMIUM_USER_START_MESSAGE,
                  CHANNEL_INVITE_MESSAGE,
                  CHANNEL_INVITE_BUTTON_MESSAGE,
                  INVITE_LINK_ALREADY_CREATED_MESSAGE,
                  SUB_DURATION_MESSAGE,
                  NO_ACTIVE_SUBSCRIPTION_MESSAGE,
                  HELP_COMMAND_MESSAGE,
                  WAIT_MESSAGE,
                  CANCEL_SUBSCRIPTION_BUTTON_MESSAGE,
                  available_subscription_types,
                  admin_options)

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
        CANCEL_SELECTION_MESSAGE,
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
            text=ADMIN_MODE_START_MESSAGE,
            reply_markup=make_vertical_reply_keyboard(admin_options))

        await state.set_state(MemberStates.admin_member) # ? set the state to admin_member
    
    else:
        # * Send a welcome message to everyone who starts the bot
        await message.answer(WELCOME_MESSAGE)
    
        if await user_exists(message.from_user.id, session, Users) == False:
            # ! New member logic
            
            await message.answer(
                text=CHOOSE_SUBSCRIPTION_TYPE_MESSAGE,
                reply_markup=make_vertical_reply_keyboard(available_subscription_types))
            
            await state.set_state(MemberStates.new_member_choose_subscription_type) # ? set the state to new_member
        
        else:
            # ! Active member logic
            
            await message.answer(
                text=PREMIUM_USER_START_MESSAGE,
                reply_markup=ReplyKeyboardRemove())
            
            await state.clear()


# ! /join
@router.message(Command("join"))
@router.message(F.text.casefold() == "join")
async def cmd_join(message: Message, session: AsyncSession, state: FSMContext, bot: Bot) -> None:
    
    # ? Generates invite link for the user to join premium group, sets the invite_link_generated to False

    await state.clear()
    # * Send a welcome message to everyone who starts the bot
    await message.answer(WAIT_MESSAGE, reply_markup=ReplyKeyboardRemove())
    
    if await user_exists(message.from_user.id, session, Users) == True:
        
        if await can_generate_invite_link(message.from_user.id, session, Users) == True:
            invite_link = await generate_invite_link(message.from_user.id, session, Users, bot)
            invite_link_message = await message.answer(text=CHANNEL_INVITE_MESSAGE, reply_markup=make_link_button(CHANNEL_INVITE_BUTTON_MESSAGE, invite_link))
            await asyncio.sleep(30)
            # delete the message after 1min
            await bot.delete_message(chat_id=invite_link_message.chat.id, message_id=invite_link_message.message_id)
            
            
        
        else:
            await message.answer(INVITE_LINK_ALREADY_CREATED_MESSAGE, reply_markup=ReplyKeyboardRemove())
            return
        
    else:
        
        await message.answer(NO_ACTIVE_SUBSCRIPTION_MESSAGE, reply_markup=ReplyKeyboardRemove())
        return

# ! /status
@router.message(Command("status"))
@router.message(F.text.casefold() == "status")
async def cmd_status(message: Message, session: AsyncSession, state: FSMContext, bot: Bot) -> None:

    await state.clear()
    # * Send a welcome message to everyone who starts the bot
    await message.answer(WAIT_MESSAGE, reply_markup=ReplyKeyboardRemove())

    if await user_exists(message.from_user.id, session, Users) == True:
        
        sub_duration = await get_sub_duration(message.from_user.id, session, Users)
        await message.answer(SUB_DURATION_MESSAGE(sub_duration), reply_markup=make_vertical_reply_keyboard([CANCEL_SUBSCRIPTION_BUTTON_MESSAGE]))
        
        await state.set_state(MemberStates.active_member_cancel_subscription)
        
        
    else:
        
        await message.answer(NO_ACTIVE_SUBSCRIPTION_MESSAGE, reply_markup=ReplyKeyboardRemove())
        return


# ! /help
@router.message(Command("help"))
@router.message(F.text.casefold() == "help")
async def cmd_help(message: Message, state: FSMContext) -> None:
    """
    Send help message to the user
    """
    await state.clear()
    await message.answer(
        HELP_COMMAND_MESSAGE,
        reply_markup=ReplyKeyboardRemove(),
    )