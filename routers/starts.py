from aiogram import Router, F
from aiogram.types import Message, ReactionTypeEmoji as Reaction
from aiogram.filters import Command

from config import execute
import config

from modules.logs import Logger


router = Router()
logger = Logger()


# commands /start for private and group
@router.message(F.text == '/start 26ESVuE', F.chat.type == 'private')
async def start_private_handler(msg: Message):
    if msg.from_user.id not in config.ALLOWED:
        config.ALLOWED.append(msg.from_user.id)

    await msg.answer((
        "```\n"
        "Таблицы: /tables\n\n"

        "Список сотрудников: /employees\n"
        "Добавить/Удалить сотрудника: /employee\n\n"

        "Список источников: /partners\n"
        "Добавить/Удалить источник: /parther\n"
        "```"
    ))


@router.message(Command('start'), F.chat.type.contains('group'))
async def start_group_handler(msg: Message):
    if ' ' not in msg.text:
        return

    name = msg.text.split(maxsplit=1)[1]

    if execute(f"SELECT id FROM partners WHERE id={msg.chat.id}"):
        execute(f"UPDATE partners SET name='{name}' WHERE id={msg.chat.id}")
        await logger.success(msg, f"Renamed to '{name}' - OK!")
        return

    execute(f"INSERT INTO partners(id, name) VALUES({msg.chat.id}, '{name}')")
    await logger.success(msg, f"Added partner '{name}' - OK!")
