# -*- coding: utf-8 -*-
from __future__ import print_function
import random
from test import *


def check_custom_slots(intent):
    code = intent['slots']['level']['resolutions']['resolutionsPerAuthority'][0]['status']['code']
    if code == "ER_SUCCESS_MATCH":
        return intent['slots']['level']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    else:
        return None


def make_question(level):
    randnum = random.randint(100, 1000)
    if level == "初級":
        level_num = 5
        answer_num = random.randint(1, level_num)
        num_list = range(1, randnum, int(randnum / level_num))
    elif level == "中級":
        level_num = 10
        answer_num = random.randint(1, level_num)
        num_list = range(1, randnum, int(randnum / level_num))
    elif level == "上級":
        level_num = 20
        answer_num = random.randint(1, level_num)
        num_list = range(1, randnum, int(randnum / level_num))
    elif level == "神級":
        level_num = 30
        answer_num = random.randint(1, level_num)
        num_list = range(1, randnum, int(randnum / level_num))

    information = {}
    random.shuffle(num_list)
    information['level'] = level
    information['level_num'] = level_num
    information['num_list'] = num_list
    information['answer_num'] = answer_num
    return information
