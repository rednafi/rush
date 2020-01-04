import sys
from collections import OrderedDict

import click
import pretty_errors

from rush_cli.read_tasks import ReadTasks
from rush_cli.utils import split_lines, strip_spaces, beautify_task_name


class PrepTasks(ReadTasks):
    """Class for preprocessing tasks before running."""

    def __init__(self, *filter_names):
        super().__init__()
        self.filter_names = filter_names

    @staticmethod
    def clean_tasks(yml_content):
        """Splitting stringified tasks into into a list of individual tasks."""
        cleaned_tasks = OrderedDict()

        for task_name, task_chunk in yml_content.items():
            if task_chunk:
                task_chunk = strip_spaces(task_chunk)
                task_chunk = split_lines(task_chunk)
                cleaned_tasks[task_name] = task_chunk
            else:
                cleaned_tasks[task_name] = ""

        return cleaned_tasks

    @classmethod
    def _replace_placeholder_tasks(cls, task_chunk: list, cleaned_tasks: dict) -> list:
        """Recursively replace dependant task names with actual task commands."""

        for idx, task in enumerate(task_chunk):
            if isinstance(task, str):
                if task in cleaned_tasks.keys():
                    task_chunk[idx] = cleaned_tasks[task]
            else:
                task_chunk[idx] = cls._replace_placeholder_tasks(task, cleaned_tasks)
        return task_chunk

    @classmethod
    def _flatten_task_chunk(cls, nested_task_chunk: list) -> list:
        """Recursively converts a nested task list to a flat list."""

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
                click.secho("Error: Task does not exist.", fg="magenta")
                sys.exit(1)
        else:
            return cleaned_tasks

    def get_prepared_tasks(self):
        """Get the preprocessed task dict."""

        yml_content = self.read_rushfile()
        cleaned_tasks = self.clean_tasks(yml_content)
        # replace placeholders and flatten
        for task_name, task_chunk in cleaned_tasks.items():
            task_chunk = self._replace_placeholder_tasks(task_chunk, cleaned_tasks)
            task_chunk = self._flatten_task_chunk(task_chunk)
            task_chunk = "\n".join(task_chunk)
            cleaned_tasks[task_name] = task_chunk

        # apply filter
        cleaned_tasks = self._filter_tasks(cleaned_tasks, *self.filter_names)
        return cleaned_tasks


class Views(PrepTasks):
    def __init__(self, *filter_names):
        super().__init__(*filter_names)
        self.filter_names = filter_names

    @property
    def view_rushpath(self):
        rushfile_path = self.find_rushfile()
        click.echo("")
        click.secho(rushfile_path, fg="yellow")
