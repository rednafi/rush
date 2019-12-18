import os
import subprocess
import sys
from collections import OrderedDict
from typing import Dict, List

import click
import colorama
import yaml

from rush.utils import run_task, split_lines, strip_spaces, check_shell

# Don't strip colors.
colorama.init(strip=False)

use_shell = check_shell()


def _read_yml():
    try:
        with open("./rushfile.yml") as file:
            yml_content = yaml.load(file, Loader=yaml.FullLoader)
        return yml_content

    except FileNotFoundError:
        sys.exit("rushfile.yml file not found")


def _clean_tasks(yml_content):
    cleaned_tasks = OrderedDict()
    try:
        for task_name, task_chunk in yml_content.items():
            task_chunk = strip_spaces(task_chunk)
            task_chunk = split_lines(task_chunk)
            cleaned_tasks[task_name] = task_chunk

        return cleaned_tasks
    except AttributeError:
        sys.exit("Rushfile is empty.")


# def replc(lst):
#     for idx, cdx in enumerate(lst):
#         if isinstance(cdx, int):
#             if cdx == 1:
#                 lst[idx] = "a"
#         else:
#             lst[idx] = replc(cdx)
#     return lst


def replc(lst, dic):
    for idx, cdx in enumerate(lst):
        if isinstance(cdx, str):
            if cdx in dic.keys():
                lst[idx] = dic[cdx]
        else:
            lst[idx] = replc(cdx)
    return lst


def flatten_nested_list(nestedList):
    """ Converts a nested list to a flat list """
    flatList = []
    # Iterate over all the elements in given list
    for elem in nestedList:
        # Check if type of element is list
        if isinstance(elem, list):
            # Extend the flat list by adding contents of this element (list)
            flatList.extend(flatten_nested_list(elem))
        else:
            # Append the elemengt to the list
            flatList.append(elem)
    return flatList


yml = _read_yml()
cleaned_tasks = _clean_tasks(yml)
for task_name, task_chunk in cleaned_tasks.items():
    l = replc(task_chunk, cleaned_tasks)
    print(l)


# m = ['task_1', 'echo "task2 is running"']
# print(replc(m, 'task_1', [1,2,3]))
