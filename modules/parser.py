from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

from typing import List, Union, Optional
from datetime import datetime as dt

from config import execute, bot

from modules.enums import STATUS


class Result:
	def __init__(self, data):
		self.rep_id = data['id']
		self.date = data['date']
		self.status = (
			STATUS.SIMPLE
			if len(data['employees']) == 1 else STATUS.MAIN
		)

		self.partner = execute(
			"SELECT name FROM partners "
			f"WHERE id={int(self.rep_id.split(':')[0])}"
		)
		self.country = data['country'].capitalize()
		self.bookmaker = data['bookmaker'].capitalize()
		self.profile = (
			data['profile']
			.replace('(', '').replace(')', '')
			.capitalize()
		)
		self.match = data['match']
		self.count = len(data['employees'])
		self.employees = data['employees']

		self.stake = float(data['stake'])
		self.coefficient = data['coefficient']
		self.profit = float(data['profit']) if data['profit'] != '' else ""
		self.refund = (
			self.stake + self.profit
			if self.profit != '' else ""
		)

		self.error = 'Да' if 'x3' in data['marks'] else 'Нет'
		self.overkill = 'Да' if 'x5' in data['marks'] else 'Нет'


class Parser:
	async def parse(self, msg: Message) -> Union[Result, Exception]:
		try:
			lines = msg.caption.split('\n')

			# line 1
			try:
				country, profile = (
					lines[0].split(maxsplit=1)
				)
			except ValueError:
				raise Exception("Нету страны или профиля")

			# line 2
			try:
				bookmaker, stake, coefficient = (
					lines[1].split()
				)
			except ValueError:
				raise Exception("Нету букмейкера, суммы или кэффа")

			# line 3
			profit = (
				float(lines[2].strip().replace(',', '.'))
				if lines[2].strip() != '' and lines[2][-1].isdigit() else ""
			)
 
			if profit != '':
				lines = msg.caption.replace('\n\n', '').split('\n')

			# line 4
			employees = [
				employee.strip()
				for employee in lines[3].split(',') if employee.strip() != ''
			]
			
			for employee in employees:
				user_id = execute(f"SELECT id FROM employees WHERE name='{employee}'")
				partner = execute(f"SELECT name FROM partners WHERE id={msg.chat.id}")

				if user_id is None:
					raise Exception(f"Сотрудника '{employee}' не существует")
 
				try:
					await bot.get_chat_member(
						msg.chat.id, user_id
					)
				except TelegramBadRequest as e:
					raise Exception(f"Сотрудника '{employee}' нету в '{partner}'")

			# last line
			marks = [
				mark.strip()
				for mark in lines[-1].split()
			]

			# mark date from line 5
			try:
				date = self.__find(marks) or msg.date.strftime("%d.%m.%Y")
			except ValueError:
				raise Exception("Неправильно написано время")

		except IndexError:
			return Exception("Отчёт неправильный (или не отчёт во все)")

		except Exception as e:
			return e

		# return result
		return Result({
			"id": f"{msg.chat.id}:{msg.message_id}",
			"date": date,
			"country": country,
			"bookmaker": bookmaker,
			"profile": profile,
			"match": "None",
			"employees": employees,

			"stake": stake,
			"coefficient": coefficient,
			"profit": profit,
			"marks": marks
		})

	def __find(self, array: List) -> Optional[str]:
		for el in array:
			if '.' in el:
				return dt.strptime(el, "%d.%m.%y").strftime("%d.%m.%Y")

		return None
