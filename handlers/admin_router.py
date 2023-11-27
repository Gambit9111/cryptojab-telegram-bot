from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
import asyncio

from aiogram.fsm.context import FSMContext

from keyboards.vertical_reply_kb import make_vertical_reply_keyboard 

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Users

from .states import MemberStates

from .functions import create_new_user, cancel_subscription

from data import (admin_options,
                  ADD_MEMBER_MESSAGE,
                  KICK_MEMBER_MESSAGE,
                  WRONG_FORMAT_MESSAGE,
                  ADDING_MEMBER_MESSAGE,
                  ADDING_MEMBER_SUCCESS_MESSAGE,
                  KICKING_MEMBER_MESSSAGE,
                  KICKING_MEMBER_SUCCESS_MESSAGE,
                  UNKNOWN_COMMAND_ERROR_MESSAGE_DISPLAY,
                  UNKNOWN_COMMAND_ERROR_MESSAGES)

router = Router(name="admin-router")

# * 1)
# ! will run after ADMIN action
@router.message(MemberStates.admin_member, F.text.in_(admin_options))
async def admin_member(message: Message, state: FSMContext):
    
    if message.text == admin_options[0]:
        # ! Add new member logic
        await message.answer(text=ADD_MEMBER_MESSAGE, reply_markup=ReplyKeyboardRemove())
        await state.set_state(MemberStates.admin_member_add_user)
    
    elif message.text == admin_options[1]:
        # ! Kick member logic
        await message.answer(text=KICK_MEMBER_MESSAGE, reply_markup=ReplyKeyboardRemove())
        await state.set_state(MemberStates.admin_member_kick_user)

# ?
@router.message(MemberStates.admin_member)
async def admin_member_unknown(message: Message):
    await message.answer(text=UNKNOWN_COMMAND_ERROR_MESSAGE_DISPLAY(UNKNOWN_COMMAND_ERROR_MESSAGES[3]), reply_markup=make_vertical_reply_keyboard(admin_options))

# * 2)
# ! will run after ADMIN action -> Add new member
@router.message(MemberStates.admin_member_add_user)
async def admin_member_add_user(message: Message, state: FSMContext, session: AsyncSession):
    
    # get the telegram_id of the user and the duration of the subscription
    # make sure we can convert the telegram_id and days to int
    try:
        telegram_id, days = message.text.split(",")
        telegram_id = int(telegram_id)
        days = int(days)
    except Exception as e:
        print("admin_member_add_user ERROR", e)
        await message.answer(text=WRONG_FORMAT_MESSAGE, reply_markup=ReplyKeyboardRemove())
        return
    
    print("telegram_id", telegram_id)
    print("days", days)
    
    await message.answer(text=ADDING_MEMBER_MESSAGE)
    await create_new_user(telegram_id, days, session, Users)
    
    await message.answer(text=ADDING_MEMBER_SUCCESS_MESSAGE, reply_markup=ReplyKeyboardRemove())
    await state.clear()

# * 3)
# ! will run after ADMIN action -> Kick member
@router.message(MemberStates.admin_member_kick_user)
async def admin_member_kick_user(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    # get the telegram_id of the user and the duration of the subscription
    # make sure we can convert the telegram_id and days to int
    try:
        telegram_id = message.text
        telegram_id = int(telegram_id)
    except Exception as e:
        print("admin_member_kick_user ERROR", e)
        await message.answer(text=WRONG_FORMAT_MESSAGE, reply_markup=ReplyKeyboardRemove())
        return
    
    print("telegram_id", telegram_id)
    await message.answer(text=KICKING_MEMBER_MESSSAGE)
    await cancel_subscription(telegram_id, session, Users, bot)
    
    await message.answer(text=KICKING_MEMBER_SUCCESS_MESSAGE, reply_markup=ReplyKeyboardRemove())
    await state.clear()