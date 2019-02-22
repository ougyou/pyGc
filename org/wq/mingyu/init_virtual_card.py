# by ougyou
# 文件格式要求id balance余额，中间与tab键分割，从数据库复制出来就是此格式
# 查询语句  select id, pay - charge from card_base where xxx;  并保存成文件
# 安装python环境,执行以下命令,文件输出到当前执行目录
# python init_virtual_card.py -f [file_path]

# -*- coding: utf-8 -*-
import argparse
import json


def get_update_sql(id, balance):
    card_num = balance // 5000
    balance_val = balance % 5000
    child_card_info = '{"balance":5000,"createTime":"2018-12-12 00:00:00","id":1001}'
    list = []
    last_card_id = 1000
    for i in range(1001, 1001 + int(card_num), 1):
        obj = json.loads(child_card_info)
        obj['id'] = i
        last_card_id = i
        list.append(obj)

    if balance_val > 0:
        obj = json.loads(child_card_info)
        obj['balance'] = balance_val
        obj['id'] = last_card_id + 1
        list.append(obj)

    update_sql = "update card_base set virtual_child_cards = '{1}' where id='{0}';".format(id, json.dumps(list));
    return update_sql


def read_data(mingyu_file):
    f = open(mingyu_file, 'r')
    res_file = open('o_init_card_virtual.sql', 'w')
    lines = f.read().splitlines()
    for line in lines:
        if line:
            line = line.strip('\n')
            print line
            info = line.split("\t");
            if len(info) == 2 and float(info[1]) > 0:
                sql = get_update_sql(info[0], float(info[1]))
                print>> res_file, sql
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, nargs='+',
                        help='指定条件下的file路径')
    args = parser.parse_args()
    read_data(args.f[0])
