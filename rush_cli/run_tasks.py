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
        is_color=True,
        print_cmd=True,
        capture_err=True,
    ):
        super().__init__(*filter_names)
        self.interactive = interactive
        self.is_color = is_color
        self.print_cmd = print_cmd
        self.capture_err = capture_err
        self.cleaned_tasks = self.get_prepared_tasks()

    def run_all_tasks(self):
        for task_name, task_chunk in self.cleaned_tasks.items():
            if task_name.startswith("//"):
                task_name = task_name.replace("//", "")
                beautify_skiptask_name(task_name, is_color=self.is_color)

            else:
                beautify_task_name(task_name, is_color=self.is_color)
                for cmd in task_chunk:
                    if self.print_cmd and cmd.startswith("#") is False:
                        beautify_cmd(cmd)
                    try:
                        run_task(
                            self.use_shell,
                            cmd,
                            interactive=self.interactive,
                            capture_err=self.capture_err,
                        )
                    except subprocess.CalledProcessError as e:
                        click.echo(e)
                        sys.exit(1)
