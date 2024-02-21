from aiogram import Dispatcher, F
from aiogram import types

import sys
import asyncio

import config
from config import execute

from modules.parser import Parser
from modules.table import Table
from modules.logs import Logger

import routers


bot = config.bot
dp = Dispatcher()

parser = Parser()
table = Table()
logger = Logger()


execute(
	"""CREATE TABLE IF NOT EXISTS reports (
		id TEXT,
		date TEXT,
		status TEXT,

		partner TEXT,
		country TEXT,
		bookmaker TEXT,
		profile TEXT,
		match TEXT,
		count INT,
		employees TEXT,

		stake TEXT,
		coefficient TEXT,
		profit TEXT,
		refund TEXT,

		error TEXT,
		overkill TEXT
	)"""
)

execute(
	"""CREATE TABLE IF NOT EXISTS partners (
		id INT,
		name TEXT
	)"""
)

execute(
	"""CREATE TABLE IF NOT EXISTS employees (
		id INT,
		name TEXT
	)"""
)


# when created new message with photo
@dp.message(F.photo.is_not(None), F.caption.is_not(None))
async def msg_handler(msg: types.Message):
	if not execute(f"SELECT id FROM partners WHERE id={msg.chat.id}"):
		return

	parsed = parser.parse(msg)

	if isinstance(parsed, Exception):
		await logger.incorrect(msg, parsed)
		return

	table.add(parsed)

	await logger.success(msg, "Created - OK!")


# when message edited (added profit etc.)
@dp.edited_message(F.photo.is_not(None), F.caption.is_not(None))
async def edited_handler(msg: types.Message):
	if not execute(f"SELECT id FROM partners WHERE id={msg.chat.id}"):
		return

	parsed = parser.parse(msg)

	if isinstance(parsed, Exception):
		await logger.incorrect(msg, parsed)
		return

	if table.exist(parsed.rep_id):
		table.update(parsed)
		await logger.success(msg, "Edited - OK!")
		return

	table.add(parsed)
	await logger.success(msg, "Created - OK!")


@dp.message(F.text == '/report', F.chat.type.contains('group'))
async def add_report_handler(msg: types.Message):
	if not execute(f"SELECT id FROM partners WHERE id={msg.chat.id}"):
		return

	if msg.from_user.id not in config.ALLOWED:
		return

	if not msg.reply_to_message:
		return

	parsed = parser.parse(msg.reply_to_message)

	if isinstance(parsed, Exception):
		await logger.incorrect(msg.reply_to_message, parsed)
		return

	if table.exist(parsed.rep_id):
		table.update(parsed)
		await logger.success(msg.reply_to_message, "Edited - OK!")
		return

	table.add(parsed)
	await logger.success(msg.reply_to_message, "Created - OK!")


@dp.message(F.text == '/del', F.chat.type.contains('group'))
async def del_report(msg: types.Message):
	if msg.from_user.id not in config.ALLOWED:
		return

	if not msg.reply_to_message:
		return

	report = msg.reply_to_message

	table.delete(f"{report.chat.id}:{report.message_id}")
	await logger.success(report, "Deleted - OK!")


def error_handler(name, exception, traceback):
	asyncio.run(logger.system(exception))


@dp.errors()
async def errors_handler(error: types.ErrorEvent):
	await logger.system(str(error.exception))


async def main():
	sys.excepthook = error_handler

	dp.include_routers(
		routers.start_router,
		routers.tables_router,
		routers.employees_router,
		routers.partners_router
	)

	await dp.start_polling(bot)


if __name__ == '__main__':
	print("Bot started!")
	asyncio.run(main())
