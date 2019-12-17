import os
import subprocess
import sys
from collections import OrderedDict
from typing import Dict, List

import click
import colorama
import yaml

from rush.utils import  run_task, split_lines, strip_spaces

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



def _term_beautify(task_name, is_color=True, is_task_name=True):
    if is_task_name:
        task_name = f"{task_name}:"
        separator_len = len(task_name) + 3
        separator = "=" * separator_len

        if is_color:
            task_name = str(click.style(task_name, fg="yellow"))
            separator = str(click.style(separator, fg="green"))

        click.echo("")
        click.echo("")
        click.echo(task_name)
        click.echo(separator)
    else:
        if is_color:
            task_name = str(click.style(task_name, fg="blue"))
        click.echo('')
        click.echo(f'|-> {task_name}')


def _run_task_chunk(cleaned_tasks, print_task=True):
    for task_name, task_chunk in cleaned_tasks.items():
        _term_beautify(task_name)
        for task in task_chunk:
            if print_task:
                _term_beautify(task, is_task_name=False)
            run_task(task)


def run_all_tasks(*filter_names):
    yml_content = _read_yml()
    cleaned_tasks = _clean_tasks(yml_content)
    filtered_tasks = _filter_tasks(cleaned_tasks, *filter_names)
    _run_task_chunk(filtered_tasks)


run_all_tasks()
