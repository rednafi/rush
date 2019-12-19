import sys

import click
import colorama
from rush.script import RunTasks

# Don't strip colors.
colorama.init(strip=False)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--color/--no-color",
    default=True,
    help="Option to color the commands.",
)
@click.option(
    "--print-cmd/--not-print-cmd",
    default=True,
    help="Option to print the executing commands.",
)
@click.option(
    "--capture-err/--ignore-err",
    default=True,
    help="Option to capture errors",
)
@click.argument("filter_names", required=False, nargs=-1)
def entrypoint(*, filter_names, color, print_cmd, capture_err):
    run_tasks_obj = RunTasks(
        *filter_names, is_color=color, print_cmd=print_cmd, capture_err=capture_err
    )
    run_tasks_obj.run_all_tasks()
