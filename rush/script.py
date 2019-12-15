import yaml
from collections import OrderedDict
import os
import subprocess
import sys
import colorama
import click

from typing import Dict, List
from rush.utils import strip_spaces, split_lines, echo_underlines, run_task

# Don't strip colors.
colorama.init(strip=False)


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


def _filter_tasks(cleaned_tasks, *filter_names):
    if filter_names:
        try:
            filtered_tasks = {k: cleaned_tasks[k] for k in filter_names}
            return filtered_tasks
        except KeyError:
            sys.exit("Task does not exist.")
    else:
        return cleaned_tasks


def _term_beautify(task_name, is_color=True):
    task_name = f"{task_name}:"
    separator_len = len(task_name) + 3
    separator = "=" * separator_len

    if is_color:
        task_name = str(click.style(task_name, fg="yellow"))
        separator = str(click.style(separator, fg="green"))

    print("")
    print(task_name)
    print(separator)


def _run_task_chunk(cleaned_tasks):
    for task_name, task_chunk in cleaned_tasks.items():
        _term_beautify(task_name)
        for task in task_chunk:
            run_task(task)


def run_all_tasks(*filter_names):
    yml_content = _read_yml()
    cleaned_tasks = _clean_tasks(yml_content)
    filtered_tasks = _filter_tasks(cleaned_tasks, *filter_names)
    _run_task_chunk(filtered_tasks)


run_all_tasks("task_1", "task_3")
