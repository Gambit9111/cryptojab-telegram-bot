from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def make_link_button(text: str, url: str) -> InlineKeyboardMarkup:
    """
    Creates inline keyboard with one button
    :param text: button text
    :param url: button url
    :return: InlineKeyboardMarkup object
    """
    keyboard = [[InlineKeyboardButton(text=text, url=url)]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)