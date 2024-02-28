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

    async def incorrect(self, msg: Optional[Message], text: str, report: Optional[list] = None):
        if not report:
            await msg.react([Reaction(emoji="👎")])

        partner = execute(
            f"SELECT name FROM partners WHERE id={msg.chat.id}"
            if not report else (
                f"SELECT name FROM partners WHERE id={int(report[0].split(':')[0])}"
            )
        )

        if report:
            report = (
                f"{report[4]} {report[6]}\n"
                f"{report[5]} {report[10]} {report[11]}\n"
                f"{report[12]}\n"
                f"{report[9]}\n"
                "..."
            )

        await bot.send_message(
            chat_id=self.id,
            text=(
                f"Incorrect report from `{partner}`\n"
                "```\n"
                f"{msg.caption if not report else report}"
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
                f"{msg.caption if not report else report}"
                "\n```\n"
                "Error\n"
                "```\n"
                f"{text}"
                "\n```"
            )
        )
