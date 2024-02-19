from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from config import execute
import config

from modules.logs import Logger


router = Router()
logger = Logger()


# list of partners and add/del commands
@router.message(Command('partners'), F.chat.type == 'private')
async def list_employees(msg: Message):
    if msg.from_user.id not in config.ALLOWED:
        return

    text = "Партнёры:\n"

    for i, info in enumerate(execute("SELECT name FROM partners", res=False)):
        text += f"{i+1}\\. `{info[0]}`\n"

    await msg.answer(text)


@router.message(Command('partner'), F.chat.type == 'private')
async def add_employee(msg: Message):
    if msg.from_user.id not in config.ALLOWED:
        return

    info = msg.text.split()

    if len(info) == 1:
        await msg.answer(
            "```\n"
            "/partner <Имя> - Удалить источник"
            "\n```"
        )

    elif len(info) == 2:
        if execute(f"SELECT id FROM partners WHERE name='{info[1]}'"):
            execute(f"DELETE FROM partners WHERE name='{info[1]}'")
            await logger.success(msg, f"Deleted partner '{info[1]}' - OK!")
