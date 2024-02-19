from aiogram.types import Message

from typing import List, Union, Optional
from datetime import datetime as dt

from config import execute

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
    def parse(self, msg: Message) -> Union[Result, Exception]:
        try:
            lines = msg.caption.split('\n')

            # line 1
            country, profile = (
                lines[0].split(maxsplit=1)
            )

            # line 2
            bookmaker, stake, coefficient = (
                lines[1].split()
            )

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
                for employee in lines[3].split(',')
            ]

            # last line
            marks = [
                mark.strip()
                for mark in lines[-1].split()
            ]

            # mark date from line 5
            date = self.__find(marks) or msg.date.strftime("%d.%m.%Y")
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
