from aiogram import Bot, Router
from aiogram.types import (
    Message,
    ReactionTypeEmoji as Reaction
)

from typing import Union, Optional

from config import bot, execute


class Logger:
    def __init__(self):
        self.id = 1004461367

    async def success(self, msg: Message, text: str):
        await msg.react([Reaction(emoji="👍")])

        text = text.replace('-', '\\-')

        await bot.send_message(
            chat_id=self.id,
            text=(
                "Success\n"
                "```\n"
                f"{msg.caption or msg.text}\n"
                "```\n"
                f"`{text}`"
            )
        )

    async def error(self, msg: Message, text: str):
        await msg.react([Reaction(emoji="👎")])

        text = text.replace('-', '\\-')

        await bot.send_message(
            chat_id=self.id,
            text=(
                "Error\n"
                "```\n"
                f"{msg.caption or msg.text}\n"
                "```\n"
                f"`{text}`"
            )
        )

    async def system(self, text: str, traceback=None):
        text = text.replace('-', '\\-')

        await bot.send_message(
            chat_id=self.id,
            text=(
                "System\n"
                "```\n"
                f"{text}\n"
                "```"
            )
        )

    async def incorrect(self, msg: Message, text: str):
        await msg.react([Reaction(emoji="👎")])
        partner = execute(f"SELECT name FROM partners WHERE id={msg.chat.id}")

        await bot.send_message(
            chat_id=self.id,
            text=(
                f"Incorrect report from `{partner}`\n"
                "```\n"
                f"{msg.caption}"
                "\n```\n"
                "Error\n"
                "```\n"
                f"{text}"
                "\n```"
            )
        )

        await bot.send_message(
            chat_id=447050022,
            text=(
                f"Incorrect report from `{partner}`\n"
                "```\n"
                f"{msg.caption}"
                "\n```\n"
                "Error\n"
                "```\n"
                f"{text}"
                "\n```"
            )
        )
