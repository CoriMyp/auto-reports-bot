from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from config import execute
import config

from modules.logs import Logger


router = Router()
logger = Logger()


# list of employees and add/del commands
@router.message(Command('employees'), F.chat.type == 'private')
async def list_employees(msg: Message):
    if msg.from_user.id not in config.ALLOWED:
        return

    text = "Сотрудники:\n"

    for i, info in enumerate(execute("SELECT name FROM employees", res=False)):
        text += f"{i+1}\\. `{info[0]}`\n"

    await msg.answer(text)


@router.message(Command('employee'), F.chat.type == 'private')
async def add_employee(msg: Message):
    if msg.from_user.id not in config.ALLOWED:
        return

    info = msg.text.split()

    if len(info) == 1:
        await msg.answer(
            "```\n"
            "/employee <Имя> <ID> - Добавить\n"
            "/employee <Имя> - Удалить\n\n"
            "Добавление/Удаление сотрудника"
            "\n```"
        )

    elif len(info) == 2:
        if execute(f"SELECT id FROM employees WHERE name='{info[1]}'"):
            execute(f"DELETE FROM employees WHERE name='{info[1]}'")
            logger.success(msg, f"Deleted employee '{info[1]}' - OK!")

    elif len(info) == 3:
        if not execute(f"SELECT id FROM employees WHERE id={int(info[2])}"):
            execute(f"INSERT INTO employees VALUES({info[2]}, '{info[1]}')")
            logger.success(msg, f"Added employee '{info[1]}' - OK!")
