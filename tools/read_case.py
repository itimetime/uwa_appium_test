# -*- coding: utf-8 -*-
# @time    : 2020/5/18 14:37
# @file    : read_case.py
import ast

import config.config
import pandas as pd
import os


# 文件过滤函数函数，Excel通过Ms—office打开会生成“~$”开头的临时文件，程序打开会报错。
def get_test_case_files():
    total_files = os.listdir(config.config.test_case_path)
    ret = []
    for file_name in total_files:
        if not file_name.startswith("~$") and (file_name.endswith(".xlsx") or file_name.endswith(".xls")):
            ret.append(file_name)
    return ret


# 获取case文件绝对路径
def get_test_case_path():
    return [os.path.join(config.config.test_case_path, file_name) for file_name in get_test_case_files()]


# 读取case文件中的case信息,并传回json信息
def read_test_case():
    case_path_list = get_test_case_path()
    case_list = []
    for case_path in case_path_list:
        f = pd.ExcelFile(case_path)
        for sheet_name in f.sheet_names:
            df = pd.read_excel(case_path, sheet_name=sheet_name)
            for i in df.index.values:  # 获取行号的索引，并对其进行遍历：
                # 根据i来获取每一行指定的数据 并利用to_dict转成字典
                # row_data = df.loc[i, df.columns].to_dict()
                row_data = df.loc[i, ['ID', 'PRECONDITION', 'DESCRIPTION']].to_dict()
                operation, element, checkpoint, check_element, expect_value = df.loc[
                    i, ["OPERATION", "ELEMENT", "CHECKPOINT", "CHECKELEMENT", "EXPECT_VALUE"]]
                actions, assertion = get_operator_steps(operation, element, checkpoint, check_element, expect_value)
                row_data["actions"] = actions
                row_data["assert"] = assertion
                case_list.append(row_data)
    return case_list


def get_operator_steps(a, b, c, d, e):
    n = 1
    actions = {}
    operations = str(a).split(",")
    if len(operations) == 1:
        elements = [str(b)]
    else:
        elements = str(b).split(",")
    asserts = str(c)
    asserts_elements = str(d)
    expect_values = str(e)
    # print(asserts,asserts_elements,expect_values)
    for i in range(len(operations)):
        all_value = elements[i].split("|")
        key_name = operations[i] + str(n)
        actions[key_name] = all_value
        n += 1
    assertion = {"checkpoint": asserts, "assert_element": asserts_elements, "expect_value": expect_values}
    # 存在多个验证将启用此段代码
    # for i in range(len(asserts)):
    #     all_value = asserts_elements[i].split("|")
    #     key_name = asserts[i] + str(n)
    #     actions[key_name] = all_value
    #     actions[key_name].append(expect_values[i])
    #     n += 1

    return actions, assertion


def get_excel_head():
    case_path = get_test_case_path()[0]
    df = pd.read_excel(case_path)
    return list(df.columns)


# 单独运行此文件的测试功能
if __name__ == '__main__':
    for case in read_test_case():
        print(case)

    print(get_excel_head())
