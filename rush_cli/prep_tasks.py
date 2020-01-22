import sys
from collections import OrderedDict

import click

from rush_cli.read_tasks import ReadTasks
from rush_cli.utils import beautify_task_cmd, beautify_task_name, scream


class PrepTasks(ReadTasks):
    """Class for preprocessing tasks before running."""

    def __init__(self, *args, no_deps=False, **kwargs):
        super().__init__(**kwargs)
        self.filter_names = args
        self.no_deps = no_deps

    @staticmethod
    def _clean_tasks(yml_content):
        """Splitting stringified tasks into into a list of individual tasks."""

        cleaned_tasks = OrderedDict()

        for task_name, task_chunk in yml_content.items():
            if task_chunk:
                task_chunk = task_chunk.rstrip()
                task_chunk = task_chunk.split("\n")
                cleaned_tasks[task_name] = task_chunk
            else:
                cleaned_tasks[task_name] = ""

        return cleaned_tasks

    def _replace_placeholder_tasks(self, task_chunk: list, cleaned_tasks: dict) -> list:
        """Recursively replace dependant task names with actual task commands."""

        for idx, task in enumerate(task_chunk):
            if isinstance(task, str):
                if task in cleaned_tasks.keys():
                    if not self.no_deps:
                        task_chunk[idx] = cleaned_tasks[task]
                    else:
                        task_chunk[idx] = ""
            else:
                task_chunk[idx] = PrepTasks._replace_placeholder_tasks(
                    task, cleaned_tasks
                )

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
                not_found_tasks = [
                    k for k in filter_names if k not in cleaned_tasks.keys()
                ]
                click.secho(
                    f"Error: Tasks {not_found_tasks} do not exist.", fg="magenta"
                )
                sys.exit(1)
        else:
            return cleaned_tasks

    def get_prepared_tasks(self):
        """Get the preprocessed task dict."""

        yml_content = self.read_rushfile()
        cleaned_tasks = self._clean_tasks(yml_content)

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
    """View ad hoc tasks."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_names = args

    @property
    def view_rushpath(self):
        rushfile_path = self.find_rushfile()
        click.secho(rushfile_path, fg="cyan")

    @property
    def view_tasks(self):
        cleaned_tasks = self.get_prepared_tasks()

        scream(what="view")
        for k, v in cleaned_tasks.items():
            beautify_task_name(k)
            beautify_task_cmd(v)

    @property
    def view_tasklist(self):
        deps = self._prep_deps()

        scream(what="list")
        click.echo()
        for k, v in deps.items():
            click.secho("-" + " " + k, fg="yellow")
            for cmd in v:
                click.echo(" " * 2 + "-" + " " + cmd)

    def _prep_deps(self):
        """Preparing a dependency dict from yml contents."""

        # reading raw rushfile as a dict
        yml_content = self.read_rushfile()

        # splitting dict values by newlines
        yml_content = {k: v.split("\n") for k, v in yml_content.items() if v}

        # finding task dependencies
        deps = {}
        for k, v in yml_content.items():
            lst = []
            for cmd in v:
                if cmd in yml_content.keys():
                    lst.append(cmd)
            deps[k] = lst

        # filter dependencies
        deps = self._filter_tasks(deps, *self.filter_names)

        return deps

    #     def _task_deps(self):
    #         """Drawing dependency graph. Need to work on this."""

    #         deps = self._prep_deps()
    #         G = nx.OrderedDiGraph()
    #         G.add_nodes_from(deps.keys())
    #         G.add_edges_from([(k, cmd) for k, v in deps.items() for cmd in v])
