import yaml
from collections import OrderedDict
import os
import subprocess

from typing import Dict, List
from rush.utils import strip_spaces, split_lines, echo_underlines, run_task


def _read_yml():
    if os.path.exists("rushfile.yml"):
        with open("./rushfile.yml") as file:
            yml_content = yaml.load(file, Loader=yaml.FullLoader)
        return yml_content

    else:
        raise FileNotFoundError("rushfile.yml file not found")


def _clean_tasks(yml_content):
    cleaned_tasks = OrderedDict()

    for task_name, task_chunk in yml_content.items():
        task_chunk = strip_spaces(task_chunk)
        task_chunk = split_lines(task_chunk)
        cleaned_tasks[task_name] = task_chunk

    return cleaned_tasks


def _run_task_chunk(cleaned_tasks, *task_names):
    if task_names:
        cleaned_tasks = {k: cleaned_tasks[k] for k in task_names}

    for task_name, task_chunk in cleaned_tasks.items():

        print_task_name = f"Executing {task_name}"
        print("" * len(print_task_name))
        print(print_task_name)
        print("=" * len(print_task_name))

        for task in task_chunk:
            run_task(task)


def run_all_tasks():
    yml_content = _read_yml()
    cleaned_tasks = _clean_tasks(yml_content)
    _run_task_chunk(cleaned_tasks, 'task_1', 'task_2')


# from pprint import pprint

# yml_content = _read_yml()
# clean_tasks = _clean_tasks(yml_content)

# pprint(yml_content)
# pprint(clean_tasks)
# pprint(_run_commands(clean_tasks))
run_all_tasks()
