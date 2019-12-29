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
        interactive=True,
        print_cmd=True,
        capture_err=True,
        view_tasks=False
    ):
        super().__init__(*filter_names)
        self.interactive = interactive
        self.print_cmd = print_cmd
        self.capture_err = capture_err
        self.cleaned_tasks = self.get_prepared_tasks()
        self.view_tasks = view_tasks

    def run_all_tasks(self):
        for task_name, task_chunk in self.cleaned_tasks.items():
            if task_name.startswith("//") and not self.view_tasks:
                task_name = task_name.replace("//", "")
                beautify_skiptask_name(task_name)

            else:
                beautify_task_name(task_name)
                for cmd in task_chunk:
                    if self.print_cmd:
                        beautify_cmd(cmd)
                    try:
                        if not self.view_tasks:
                            run_task(
                                self.use_shell,
                                cmd,
                                interactive=self.interactive,
                                capture_err=self.capture_err,
                            )
                    except subprocess.CalledProcessError as e:
                        click.echo(e)
                        sys.exit(1)
