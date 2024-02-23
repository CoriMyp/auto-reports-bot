import openpyxl as xl
from aiogram.exceptions import TelegramBadRequest

from datetime import datetime as dt
from typing import List

import os
import shutil

from modules.parser import Result
from config import execute, bot


class Table:
	def __init__(self):
		self.count = len(execute(
			"SELECT * FROM reports",
			res=False
		) or [])

	def save(self):
		shutil.copy(
			os.path.realpath("database.db"), "tables/"
		)

	def add(self, parsed: Result):
		execute(f"""INSERT INTO reports VALUES(
			'{parsed.rep_id}',
			'{parsed.date}',
			'{parsed.status.value}',

			'{parsed.partner}',
			'{parsed.country}',
			'{parsed.bookmaker}',
			'{parsed.profile}',
			'{parsed.match}',
			{parsed.count},
			'{",".join(parsed.employees)}',

			'{parsed.stake}',
			'{parsed.coefficient}',
			'{parsed.profit}',
			'{parsed.refund}',

			'{parsed.error}',
			'{parsed.overkill}'
		)""")

		self.save()

	def update(self, parsed: Result):
		execute(f"""UPDATE reports SET
			date='{parsed.date}',
			status='{parsed.status.value}',

			partner='{parsed.partner}',
			country='{parsed.country}',
			bookmaker='{parsed.bookmaker}',
			profile='{parsed.profile}',
			match='{parsed.match}',
			count={parsed.count},
			employees='{",".join(parsed.employees)}',

			stake='{parsed.stake}',
			coefficient='{parsed.coefficient}',
			profit='{parsed.profit}',
			refund='{parsed.refund}',

			error='{parsed.error}',
			overkill='{parsed.overkill}'

			WHERE id='{parsed.rep_id}'
		""")

		self.save()

	def delete(self, rep_id: str):
		execute(f"DELETE FROM reports WHERE id='{rep_id}'")

	def exist(self, rep_id: str) -> bool:
		return execute(
			f"SELECT id FROM reports WHERE id='{rep_id}'"
		) is not None

	async def gather(self, filters: List[str]):
		shutil.copy(
			os.path.realpath("tables/clean/main_table.xlsx"), "tables/"
		)
		shutil.copy(
			os.path.realpath("tables/clean/bot_table.xlsx"), "tables/"
		)

		main_table = xl.load_workbook("tables/main_table.xlsx")
		bot_table = xl.load_workbook("tables/bot_table.xlsx")

		mpage = main_table.active
		bpage = bot_table.active

		filters = [filter for filter in filters if filter != '']

		# gather main table
		mrow, brow = 2, 2

		for i, info in enumerate(
			execute(
				f"SELECT * FROM reports WHERE {' AND '.join(filters)}"
				if filters[0] != 'all' else "SELECT * FROM reports",
				res=False
			)
		):
			group = await bot.get_chat(int(info[0].split(':')[0]))
			group_id = group.id

			print(group.title, group.type, group.id, int(info[0].split(':')[0]))

			mpage[f'A{mrow}'].value = info[1]
			mpage[f'B{mrow}'].value = info[2]
			mpage[f'C{mrow}'].value = info[3]
			mpage[f'D{mrow}'].value = info[4]
			mpage[f'E{mrow}'].value = info[5]
			mpage[f'F{mrow}'].value = info[6]
			mpage[f'G{mrow}'].value = info[7]
			mpage[f'H{mrow}'].value = int(info[8])
			mpage[f'I{mrow}'].value = float(info[11])
			mpage[f'J{mrow}'].value = info[9].split(',')[0]
			mpage[f'K{mrow}'].value = "{:.2f}".format(float(info[10]))
			mpage[f'L{mrow}'].value = (
				"{:.2f}".format(float(info[12]))
				if info[12] != '' else ""
			)
			mpage[f'M{mrow}'].value = (
				"{:.2f}".format(float(info[13]))
				if info[13] != '' else ""
			)
			mpage[f'N{mrow}'].value = info[14]
			mpage[f'O{mrow}'].value = info[15]

			mrow += 1

			if info[2] == 'Обычный':
				bpage[f'A{brow}'].value = info[1]
				bpage[f'B{brow}'].value = info[3]
				bpage[f'C{brow}'].value = info[4]
				bpage[f'D{brow}'].value = info[5]
				bpage[f'E{brow}'].value = info[6]
				bpage[f'F{brow}'].value = (
					(await bot.get_chat_member(
						chat_id=group_id,
						user_id=execute(
							"SELECT id FROM employees "
							f"WHERE name='{info[9].split(',')[0]}'"
						)
					)).user.username
				)
				bpage[f'G{brow}'].value = float(info[10])
				bpage[f'H{brow}'].value = (
					float(info[13]) if info[13] != '' else ""
				)
				bpage[f'I{brow}'].value = info[14]

				brow += 1


			if info[2] == "Основной":
				for i, employee in enumerate(info[9].split(',')):
					mpage[f'A{mrow}'].value = info[1]
					mpage[f'B{mrow}'].value = "Подотчет"
					mpage[f'C{mrow}'].value = info[3]
					mpage[f'D{mrow}'].value = info[4]
					mpage[f'E{mrow}'].value = info[5]
					mpage[f'F{mrow}'].value = info[6]
					mpage[f'G{mrow}'].value = info[7]
					mpage[f'H{mrow}'].value = 1
					mpage[f'I{mrow}'].value = float(info[11])
					mpage[f'J{mrow}'].value = employee
					mpage[f'K{mrow}'].value = (
						"{:.2f}".format(float(info[10]) / info[8])
					)
					mpage[f'L{mrow}'].value = (
						"{:.2f}".format(float(info[12]) / info[8])
						if info[12] != '' else ""
					)
					mpage[f'M{mrow}'].value = (
						"{:.2f}".format(float(info[13]) / info[8])
						if info[13] != '' else ""
					)
					mpage[f'N{mrow}'].value = info[14]
					mpage[f'O{mrow}'].value = info[15]

					bpage[f'A{brow}'].value = info[1]
					bpage[f'B{brow}'].value = info[3]
					bpage[f'C{brow}'].value = info[4]
					bpage[f'D{brow}'].value = info[5]
					bpage[f'E{brow}'].value = info[6]
					bpage[f'F{brow}'].value = (
						(await bot.get_chat_member(
							chat_id=group_id,
							user_id=execute(
								"SELECT id FROM employees "
								f"WHERE name='{employee}'"
							)
						)).user.username
					)
					bpage[f'G{brow}'].value = (
						"{:.2f}".format(
							float(info[10]) / info[8]
						)
					)
					bpage[f'H{brow}'].value = (
						"{:.2f}".format(float(info[13]) / info[8])
						if info[13] != '' else ""
					)
					bpage[f'I{brow}'].value = info[14]

					mrow += 1
					brow += 1

		main_table.save("tables/main_table.xlsx")
		bot_table.save("tables/bot_table.xlsx")
