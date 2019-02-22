# -*- coding: utf-8 -*-

from entity import UserInfo
from entity import Template
from entity import UserHistory
from difflib import SequenceMatcher
import random

TITLES = ['经理', '高级', '中级', '初级']


def read_info(user_path, template_path, history_path):
    user_list = []
    template_list = []
    history_list = []
    f = open(user_path, 'r')
    while True:
        line = f.readline()
        if line:
            line = line.strip('\n')
            info = line.split("\t", 4)
            # parse line data into user model
            if len(info) == 5:
                _user_info = UserInfo(info[0], info[1], info[2], '男', info[3], info[4])
                user_list.insert(0, _user_info)
        else:
            break

    f = open(template_path, "r")
    while True:
        line = f.readline()
        if line:
            line = line.strip('\n')
            info = line.split("\t", 3)
            # parse line data into template model
            if len(info) == 3:
                _template_info = Template(info[0], info[1], info[2])
                template_list.append(_template_info)
        else:
            break

    f = open(history_path, "r")
    while True:
        line = f.readline()
        if line:
            line = line.strip('\n')
            info = line.split("\t", 3)
            # parse line data into history model
            if len(info) == 3:
                _user_history = UserHistory(info[0], info[1], info[2])
                history_list.append(_user_history)
        else:
            break

    return user_list, template_list, history_list


# get template via [title \[company_age]] desc
def get_suitable_template(user_info, template_list, history_list):
    title = user_info.title
    # todo next higher title
    matched_level = [tmp for tmp in TITLES if not title.find(tmp)]
    if not matched_level:
        return
    idx = TITLES.index(matched_level[0])
    if idx != 0:
        matched_level.append(TITLES[idx - 1])

    matched_template = []
    for template in template_list:
        if template.age_regular.match(user_info.company_age) and template.title_regular.match(title)\
                and any((template.title.find(x) != -1) for x in matched_level):
            matched_template.append(template)

    merit_list = []
    for template in matched_template:
        merit_val = template.generate(user_info)
        if similar(merit_val, history_list) < 0.85:
            merit_list.append(merit_val)

    # random get from merit list
    if merit_list:
        return random.choice(merit_list)
    return


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
