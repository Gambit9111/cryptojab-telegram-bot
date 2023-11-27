from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.context import FSMContext

from keyboards.vertical_reply_kb import make_vertical_reply_keyboard

from data import confirmation_messages, cancel_subscription_confirmation_messages

from .states import MemberStates

from .functions import cancel_subscription

from data import (
    CANCEL_SUBSCRIPTION_BUTTON_MESSAGE,
    CANCEL_SUBSCRIPTION_CONFIRMATION_MESSAGE,
    SUBSCRIPTION_CANCELED_MESSAGE,
    SUBSCRIPTION_NOT_CANCELED_MESSAGE,
    UNKNOWN_COMMAND_ERROR_MESSAGE_DISPLAY,
    UNKNOWN_COMMAND_ERROR_MESSAGES,
)

from db.models import Users



router = Router(name="cancel-sub-router")

@router.message(MemberStates.active_member_cancel_subscription, F.text.in_([CANCEL_SUBSCRIPTION_BUTTON_MESSAGE]))
async def cancel_subscription_router(message: Message, state: FSMContext):
    
    await message.answer(text=CANCEL_SUBSCRIPTION_CONFIRMATION_MESSAGE, reply_markup=make_vertical_reply_keyboard(cancel_subscription_confirmation_messages))
    await state.set_state(MemberStates.active_member_cancel_subscription_confirm)


@router.message(MemberStates.active_member_cancel_subscription)
async def cancel_subscription_unknown(message: Message):
    await message.answer(text=UNKNOWN_COMMAND_ERROR_MESSAGE_DISPLAY(UNKNOWN_COMMAND_ERROR_MESSAGES[3]), reply_markup=make_vertical_reply_keyboard(confirmation_messages))


@router.message(MemberStates.active_member_cancel_subscription_confirm, F.text.in_(cancel_subscription_confirmation_messages))
async def cancel_subscription_confirmed(message: Message, session: AsyncSession, state: FSMContext, bot: Bot):
    
    if message.text == cancel_subscription_confirmation_messages[0]:
        await cancel_subscription(message.from_user.id, session, Users, bot)
        await message.answer(text=SUBSCRIPTION_CANCELED_MESSAGE, reply_markup=ReplyKeyboardRemove())
        await state.clear()
    
    elif message.text == cancel_subscription_confirmation_messages[1]:
        await message.answer(text=SUBSCRIPTION_NOT_CANCELED_MESSAGE, reply_markup=ReplyKeyboardRemove())
        await state.clear()

    else:
        await message.answer(text=UNKNOWN_COMMAND_ERROR_MESSAGE_DISPLAY(UNKNOWN_COMMAND_ERROR_MESSAGES[3]), reply_markup=make_vertical_reply_keyboard(cancel_subscription_confirmation_messages))