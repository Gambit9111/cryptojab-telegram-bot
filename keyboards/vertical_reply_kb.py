from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def make_vertical_reply_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Creates reply keyboard with buttons stacked vertically
    :param items: list of button names
    :return: ReplyKeyboardMarkup object
    """
    keyboard = [[KeyboardButton(text=item)] for item in items]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)