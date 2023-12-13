from aiogram import Bot


async def set_description(bot: Bot):
    """
    Sets bot description
    :param bot: Bot instance
    """
    await bot.set_my_name("CryptoJab_VIP")
    await bot.set_my_description("This bot is used to purchase subscription to CryptoJab VIP channel.")
    await bot.set_my_short_description("CryptoJab VIP channel subscription bot")