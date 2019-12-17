import sys

import click
import colorama
from rush.script import run_all_tasks

# + Executing random/entrypoints:


# Don't strip colors.
colorama.init(strip=False)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--print_command", default=True, help="Option to print/supress the commands."
)
@click.option("--capture_error", default=True, help="Option to capture/ignore error")
@click.argument("filter_names", required=False, nargs=-1)
def entrypoint(*, filter_names, print_command, capture_error):

    if print_command == "y":
        is_print_cmd = True
    elif print_command == "n":
        is_print_cmd = False

    if capture_error == "y":
        capture_error = True
    elif capture_error == "n":
        capture_error = False

    run_all_tasks(*filter_names, is_print_cmd=is_print_cmd, capture_error=capture_error)
