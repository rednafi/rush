import subprocess
import sys

import click

from rush_cli.prep_tasks import PrepTasks
from rush_cli.utils import (
    beautify_cmd,
    beautify_skiptask_name,
    beautify_task_name,
    run_task,
)


class RunTasks(PrepTasks):
    """Class for running the cleaned, flattened & filtered tasks."""

    def __init__(
        self,
        *filter_names,
        show_outputs=True,
        show_commands=True,
        catch_errors=True,
        view_tasks=False
    ):
        super().__init__(*filter_names)
        self.show_outputs = show_outputs
        self.show_commands = show_commands
        self.catch_errors = catch_errors
        self.cleaned_tasks = self.get_prepared_tasks()
        self.view_tasks = view_tasks

    def run_all_tasks(self):
        for task_name, task_chunk in self.cleaned_tasks.items():
            if task_name.startswith("//") and not self.view_tasks:
                task_name = task_name.replace("//", "")
                beautify_skiptask_name(task_name)

            else:
                if self.view_tasks:
                    click.echo("")
                    beautify_task_name(task_name)
                else:
                    beautify_task_name(task_name)

                for cmd in task_chunk:
                    if self.show_commands:
                        beautify_cmd(cmd)

                    if not self.view_tasks:
                        try:
                            run_task(
                                self.use_shell,
                                cmd,
                                interactive=self.show_outputs,
                                catch_error=self.catch_errors,
                            )
                        except subprocess.CalledProcessError as e:
                            click.echo(e)
                            sys.exit(1)
