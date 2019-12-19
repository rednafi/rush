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


class PrepTasks:
    """Class for preprocessing tasks before running."""

    def __init__(self, *filter_names):
        self.use_shell = check_shell()
        self.filter_names = filter_names

    def _read_yml(self):
        try:
            with open("./rushfile.yml") as file:
                yml_content = yaml.load(file, Loader=yaml.FullLoader)
            return yml_content

        except FileNotFoundError:
            sys.exit("rushfile.yml file not found")

    @staticmethod
    def _clean_tasks(yml_content):
        """Splitting stringified tasks into into a list of individual tasks."""
        cleaned_tasks = OrderedDict()

        try:
            for task_name, task_chunk in yml_content.items():
                task_chunk = strip_spaces(task_chunk)
                task_chunk = split_lines(task_chunk)
                cleaned_tasks[task_name] = task_chunk

            return cleaned_tasks
        except AttributeError:
            sys.exit("Rushfile is empty.")

    @classmethod
    def _replace_placeholder_tasks(cls, task_chunk: list, cleaned_tasks: dict) -> list:
        "Recursively replace dependant task names with actual task commands."

        for idx, task in enumerate(task_chunk):
            if isinstance(task, str):
                if task in cleaned_tasks.keys():
                    task_chunk[idx] = cleaned_tasks[task]
            else:
                task_chunk[idx] = cls._replace_placeholder_tasks(task, cleaned_tasks)
        return task_chunk

    @classmethod
    def _flatten_task_chunk(cls, nested_task_chunk: list) -> list:
        """ Recursively converts a nested task list to a flat list """

        flat_task_chunk = []
        for elem in nested_task_chunk:
            if isinstance(elem, list):
                flat_task_chunk.extend(cls._flatten_task_chunk(elem))
            else:
                flat_task_chunk.append(elem)
        return flat_task_chunk

    @staticmethod
    def _filter_tasks(cleaned_tasks: dict, *filter_names) -> dict:
        """Filter tasks selected by the user."""

        if filter_names:
            try:
                filtered_tasks = {k: cleaned_tasks[k] for k in filter_names}
                return filtered_tasks
            except KeyError:
                sys.exit("Task does not exist.")
        else:
            return cleaned_tasks

    def get_tasks(self):
        """Get the preprocessed task dict"""

        yml_content = self._read_yml()
        cleaned_tasks = self._clean_tasks(yml_content)

        # replace placeholders and flatten
        for task_name, task_chunk in cleaned_tasks.items():
            task_chunk = self._replace_placeholder_tasks(task_chunk, cleaned_tasks)
            task_chunk = self._flatten_task_chunk(task_chunk)
            cleaned_tasks[task_name] = task_chunk

        # apply filter
        cleaned_tasks = self._filter_tasks(cleaned_tasks, *self.filter_names)
        return cleaned_tasks


class RunTasks(PrepTasks):
    """Class for running the cleaned, flattened & filtered tasks."""

    def __init__(self, *filter_names, is_color=True, print_cmd=True, capture_err=True):
        super().__init__(*filter_names)
        self.is_color = is_color
        self.print_cmd = print_cmd
        self.capture_err = capture_err
        self.cleaned_tasks = self.get_tasks()

    def _term_beautify(self, task_name, is_task_name=True):
        if is_task_name:
            task_name = f"{task_name}:"
            separator_len = len(task_name) + 3
            separator = "=" * separator_len

            if self.is_color:
                task_name = str(click.style(task_name, fg="yellow"))
                separator = str(click.style(separator, fg="green"))

            click.echo("")
            click.echo(task_name)
            click.echo(separator)

        else:
            separator = "=>"
            if self.is_color:
                task_name = str(click.style(task_name, fg="blue"))
                separator = str(click.style(separator, fg="blue"))
            click.echo(f"{separator} {task_name}")

    def run_all_tasks(self):
        for task_name, task_chunk in self.cleaned_tasks.items():
            self._term_beautify(task_name)
            for cmd in task_chunk:
                if self.print_cmd and cmd.startswith("#") is False:
                    self._term_beautify(cmd, is_task_name=False)
                try:
                    run_task(self.use_shell, cmd, capture_err=self.capture_err)
                except subprocess.CalledProcessError as e:
                    click.echo(e)
                    sys.exit(1)
