# -*- coding: utf-8 -*-
import argparse
import random
import traceback

import MySQLdb

member_list = range(1, 1000)


def init_demo(conn, cur):

    # init the base info about account_type and for each to insert the master and card_account.
    cur.execute("INSERT INTO card_account_type(`hotel_group_id`, `hotel_id`, `default_name`, `tag`, `valid_days`,"
               " `create_user`, `create_datetime`, `modify_user`, `modify_datetime`)"
               "VALUES ('2', '0', '面积账户', 'AREA', '365', 'ADMIN', '2018-07-02 00:00:00', 'ADMIN', '2018-07-02 00:00:00') ");

    member_id = member_list[int(random.random() * 999)]
    card_no = 1000000200000000
    card_id = 200000000
    accnt_id = 100000000

    for i in range(1, 500000):
        try:
            card_no = card_no + i
            card_id = card_id + i
            accnt_id = accnt_id + i
            # 每个卡对应一个对用类型的扩展账户  为了简化卡扩展   仅对cardbase进行数据初始化，仅保证扩展数据查询的完整性.
            cur.execute("INSERT INTO card_base(`hotel_group_id`, `hotel_id`, `id`, `member_id`, `card_no`, `card_no2`, `inner_card_no`, `card_master`, `sta`, `card_type`, `card_level`, `card_src`, `card_name`, `ratecode`, `posmode`, `code3`, `code4`, `code5`, `code6`, `date_begin`, `date_end`, `password`, `salesman`, `extra_flag`, `card_flag`, `crc`, `remark`, `point_pay`, `point_charge`, `point_last_num`, `point_last_num_link`, `charge`, `pay`, `freeze`, `credit`, `receipt`, `real_pay`, `last_num`, `last_num_link`, `sta_trans_date`, `create_user`, `create_datetime`, `iss_hotel`, `create_user2`, `create_datetime2`, `modify_user2`, `modify_datetime2`, `modify_user`, `modify_datetime`) "
                       "VALUES ('2', '0', %s, %s, %s, '', %s, '', 'I', 'LPC', 'LPC1', '', '', 'RACK', '', NULL, NULL, NULL, NULL, '2017-01-12 15:05:58', '2047-01-13 15:05:58', '697281', '', '', '', '', '', '0.00', '0.00', '0', '0', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0', '0', NULL, 'WEB', '2018-07-02 00:00:00', 'LYG', '', '2018-07-02 00:00:00', '', '2018-07-02 00:00:00', 'WEB', '2018-07-02 00:00:00')",
                        [card_id, member_id, card_no, card_id])

            # 动态构造扩展数据
            pay = int(random.random() * 1000 + 200)
            charge = int(random.random() * 150 + 30)
            spec_info = '{"pay": ' + str(pay) + ', "charge": ' + str(charge) + ', "area": ' + str(pay - charge) + ', "unit": "平方", "rate": "1:10 ", "isBind": 1}'
            cur.execute("INSERT INTO card_account_master(`hotel_group_id`, `hotel_id`, `id`, `card_id`, `member_id`, `name`, `sta`, `charge`, `pay`, `credit`, `freeze`, `tag`, `spec_info`, `remark`, `create_user`, `create_datetime`, `modify_user`, `modify_datetime`) "
                        "VALUES ('2', '0', %s, %s, %s, '主帐户', 'I', '11.00', '4999.00', '110', '0', 'AREA', %s, 'demo数据初始化', 'ADMIN', '2018-07-02 00:00:00', 'ADMIN', '2018-07-02 00:00:00')", [accnt_id, card_id, member_id, spec_info])

            for j in range(1, 10):
                number = accnt_id + j
                cur.execute("INSERT INTO `card_account` (`hotel_group_id`, `hotel_id`, `card_no`, `card_id`, `member_id`, `accnt`, `number`, `number_accnt`, `link_id`, `ta_code`, `ta_descript`, `ta_descript_en`, `charge`, `charge_cash`, `charge_treat`, `source`, `source_accnt`, `source_accnt_sub`, `source_accnt_id`, `roomno`, `pay`, `accept_bank`, `balance`, `biz_date`, `gen_date`, `cashier`, `act_flag`, `ta_remark`, `ta_no`, `remark`, `ismanual`, `times_pay`, `times_charge`, `times_balance`, `trans_flag`, `trans_accnt`, `close_flag`, `close_id`, `create_user`, `create_datetime`, `modify_user`, `modify_datetime`) "
                            "VALUES ('2', '12', %s, %s, %s, %s, %s, '4', NULL, 'CA', '现金', '现金', '0.00', '0.00', '0.00', 'OWN', NULL, NULL, NULL, NULL, '300.00', '', '1066.00', '2016-11-03 00:00:00', '2016-11-03 00:00:00', '1', 'PA', '', '', NULL, 'INPUT', '0', '0', NULL, NULL, NULL, NULL, NULL, 'ADMIN', '2018-07-02 00:00:00', 'ADMIN', '2018-07-02 00:00:00')", [card_no, card_id, member_id, accnt_id, number])

            if i > 2 and i % 1000 == 0:
                conn.commit()
        except Exception, e:
            print 'str(Exception):\t', str(Exception)
            print 'str(e):\t\t', str(e)
            print 'repr(e):\t', repr(e)
            print 'e.message:\t', e.message
            print 'traceback.print_exc():'
            print 'traceback.format_exc():\n%s' % traceback.format_exc()
            card_no = card_no + 10000
            card_id = card_id + 10000
            accnt_id = accnt_id + 10000
            print card_id, card_no, accnt_id


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', type=str, nargs='+', help='mysql host', default='localhost')
    parser.add_argument('-P', type=str, nargs='+', help='mysql port', default='3306')
    parser.add_argument('-u', type=str, nargs='+', help='mysql connect user', default='root')
    parser.add_argument('-p', type=str, nargs='+', help='mysql password', default='deviskaifa')
    parser.add_argument('-db', type=str, nargs='+', help='mysql connect database', default='portal_member')
    args = parser.parse_args()

    conn = MySQLdb.connect(host=args.host[0], port=int(args.P), user=str(args.u), passwd=str(args.p), db=args.db[0], charset='utf8')

    cur = conn.cursor()

    init_demo(conn, cur)
    conn.commit()

    cur.close()
    conn.close()


