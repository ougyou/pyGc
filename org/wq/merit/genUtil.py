# -*- coding: utf-8 -*-
import argparse

import readData


def gen_merit(user_path, template_path, history_path):
    res = readData.read_info(user_path, template_path, history_path)

    user_list = res[0]
    template_list = res[1]
    history_list = res[2]

    #  1 find the history info and generate the appropriate template merits
    #  2 get the similar percent with the generated merits and get the info with min percent.
    for user_tmp in user_list:
        name = user_tmp.name
        matched_history = [tmp for tmp in history_list if name == tmp.name]
        gen_info = readData.get_suitable_template(user_tmp, template_list, matched_history)
        print gen_info

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="some information here")
    parser.add_argument('-files', type=str, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('-r', type=str, nargs='+',
                        help='relative_path')
    args = parser.parse_args()
    files = args.files
    relative_prefix_path = args.r[0] + '\\'
    gen_merit(relative_prefix_path + files[0], relative_prefix_path + files[1], relative_prefix_path + files[2])
