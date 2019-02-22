# -*- coding: utf-8 -*-

import argparse
import re

from decimal import Decimal

upgrade_list = []
db_info = {}

adjust_levels = []


def read_data(mingyu_file):

    f = open(mingyu_file, 'r')
    lines = f.read().splitlines()
    for line in lines:
        if line:
            line = line.strip('\n')
            pattern = '{"amount":([-\d.]*),"cardId":(\d*),"nights":([\d.]*),"timesIn":([\d.]*)}';
            print line
            info = re.findall(pattern, line)[0];
            # parse line data into user model
            if len(info) == 4:
                _upgrade_info = UpgradeInfo(info[1], info[0], info[2], info[3])
                if _upgrade_info.is_ok():
                    upgrade_list.insert(0, _upgrade_info)
        else:
            break
    return


# map
#     cardId  : card_level
def read_db(db_file):
    f = open(db_file, 'r')
    lines = f.read().splitlines()
    for line in lines:
        info = line.split("\t", 2)
        if len(info) == 2:
            db_info[info[0]] = info[1]


class UpgradeInfo:
    def __init__(self, card_id, amount, nights, times_in, level=None):
        self.card_id = card_id
        self.amount = amount
        self.nights = nights
        self.times_in = times_in
        self.level = level

    def matched_level(self):
        self.level = upgrade_rules[-1].level    # set the default level
        for rule in upgrade_rules:
            if Decimal(self.amount) >= rule.amount or Decimal(self.nights) >= rule.nights or Decimal(self.times_in) >= rule.times_in:
                self.level = rule.level
                return

    def is_ok(self):
        if (Decimal(self.amount) == 0) and (Decimal(self.nights) == 0) and (Decimal(self.times_in) == 0):
            return False
        return True

    def __str__(self):
        return 'card:{} \t amount:{} \t nights:{} \t timesIn:{} \t level:{}'.format(self.card_id, self.amount, self.nights, self.times_in, self.level)


upgrade_rules = [UpgradeInfo('', 20000, 20, 10, 'PD'),
                 UpgradeInfo('', 10000, 10, 5, 'PG'),
                 UpgradeInfo('', 0, 0, 0, 'PS')]


def compare():
    for _upgrade_info in upgrade_list:
        card_id = _upgrade_info.card_id
        # get the actual level compare with level rules
        _upgrade_info.matched_level()

        if db_info.get(card_id) != _upgrade_info.level:
            adjust_info = str(_upgrade_info) + "\t but db level : " + db_info.get(card_id)
            print adjust_info
            adjust_levels.insert(0, adjust_info)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('-r', type=str, nargs='+',
                        help='relative_path')
    args = parser.parse_args()
    path = args.r[0] + '\\'

    # read info from db and upgrade info, and compare to get the error upgrade infos.
    read_db(path + args.f[1])
    read_data(path + args.f[0])

    compare()

    result_file = open('mingyu_result', 'w')
    for item in adjust_levels:
        print>> result_file, item



