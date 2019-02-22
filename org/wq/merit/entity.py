# -*- coding: utf-8 -*-
import re


class UserInfo:
    def __init__(self, name, department, title, sex, board_date, company_age):
        self.name = name
        self.department = department
        self.title = title
        self.sex = sex
        self.board_date = board_date
        self.company_age = company_age


class Template:

    age_regular = ''
    title_regular = ''

    def __init__(self, company_age, title, template):
        # regular expression for range of the company_age
        self.company_age = company_age
        self.title = title
        self.template = template
        self.age_regular = re.compile(company_age)
        self.title_regular = re.compile(title)

    def generate(self, user_info):
        template = self.template
        gen_info = template.replace('#NAME', user_info.name[3:])
        gen_info = gen_info.replace('#BOARD_DATE', user_info.board_date.replace('/', '年', 1).replace('/', '月', 1))
        gen_info = gen_info.replace('#COMPANY_AGE', user_info.company_age)
        return gen_info


class UserHistory:
    def __init__(self, name, title, merit_history):
        self.name = name
        self.title = title
        self.merit_history = merit_history
