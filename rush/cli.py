import sys

import click
import colorama
from rush.script import run_all_tasks

# + Executing random/entrypoints:


# Don't strip colors.
colorama.init(strip=False)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--print-cmd/--not-print-cmd",
    default=True,
    help="Option to print/supress the commands.",
)
@click.option(
    "--capture-err/--not-capture-err",
    default=True,
    help="Option to capture/ignore error",
)
@click.argument("filter_names", required=False, nargs=-1)
def entrypoint(*, filter_names, print_cmd, capture_err):
    
    run_all_tasks(*filter_names, print_cmd=print_cmd, capture_err=capture_err)
