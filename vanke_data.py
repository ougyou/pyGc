# -*- coding: utf-8 -*-

import argparse
import re

from decimal import Decimal

all_map = {}
result_map = {}
role_list = []


def read_data():
    role_file = "resource/vanke_role"
    info_file = "resource/vanke_all"

    f = open(info_file, 'r')
    lines = f.read().splitlines()
    for line in lines:
        info = line.split("\t", 2)
        if len(info) == 2:
            all_map[info[0]] = info[1]

    rf = open(role_file, 'r')
    lines = rf.read().splitlines()
    for line in lines:
        if line:
            line = line.strip('\n')
            info = line.split("\t", 3)
            if len(info) == 3:
                info_ = result_map[info[0]]
                if info_:

                    result_map[all_map[info[0]]] = _role_info

                _role_info = RoleInfo(all_map[info[0]], info[1], info[0], info[2], info[3])

        else:
            break
    return


class RoleInfo:
    def __init__(self, date, all, role1, role2, no_role):
        self.date = date
        self.all = all
        self.role1 = role1
        self.role2 = role2
        self.no_role = no_role

    def __str__(self):
        return 'card:{} \t amount:{} \t nights:{} \t timesIn:{} \t level:{}'.format(self.card_id, self.amount, self.nights, self.times_in, self.level)

if __name__ == "__main__":
    read_data()

    result_file = open('mingyu_result', 'w')
    for item in adjust_levels:
        print>> result_file, item


