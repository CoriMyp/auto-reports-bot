from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from os import path

import config

from modules.table import Table


router = Router()
table = Table()


# send tables from /tables/<date> by date
@router.message(Command('tables'), F.chat.type == 'private')
async def send_tables(msg: Message):
    if msg.from_user.id not in config.ALLOWED:
        return

    filters = msg.text.replace('/tables', '').split(',')

    if filters[0] == '':
        await msg.answer(
            "```\n"
            "/tables <Фильтры>\n\n"
            "Возможные фильтры:\n"
            "date - дата отчёта ('01.01.2024')\n"
            "status - статус ('Обычный' или 'Основной')\n"
            "partner - источник (пример: 'Вова')\n"
            "country - страна (пример: 'Испания')\n"
            "bookmaker - букмекер (пример: 'bet365')\n"
            "profile - профиль (пример: 'any48')\n"
            "count - кол-во сотрудников\n"
            "error - ошибка ('Да' или 'Нет')\n"
            "overkill - перебор ('Да' или 'Нет')\n\n"
            "Пример:\n"
            "/tables all\n"
            "/tables date='01.01.2024', status='Обычный', count=1\n\n"
            "Выводит таблицы применяя фильтры"
            "\n```"
        )

    else:
        await table.gather([f.strip() for f in filters])

        await msg.answer_document(
            document=FSInputFile("tables/main_table.xlsx"),
            caption="Таблица бугалтерии"
        )

        await msg.answer_document(
            document=FSInputFile("tables/bot_table.xlsx"),
            caption="Таблица для бота"
        )
