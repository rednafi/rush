import sys

import click
import colorama
from click_help_colors import HelpColorsCommand

from rush_cli.prep_tasks import Views
from rush_cli.run_tasks import RunTasks

# Don't strip colors.
colorama.init(strip=False)

VERSION = "0.4.2"


@click.command(
    context_settings=dict(
        help_option_names=["-h", "--help"], token_normalize_func=lambda x: x.lower()
    ),
    cls=HelpColorsCommand,
    help_headers_color="yellow",
    help_options_color="green",
)
@click.option(
    "--all", "-a", is_flag=True, default=None, multiple=True, help="Run all tasks"
)
@click.option(
    "--hide-outputs",
    is_flag=True,
    default=True,
    help="Option to hide interactive output",
)
@click.option(
    "--ignore-errors", is_flag=True, default=None, help="Option to ignore errors"
)
@click.option(
    "--path",
    "-p",
    is_flag=True,
    default=None,
    help="Show the absolute path of rushfile.yml",
)
@click.option(
    "--no-deps", is_flag=True, default=None, help="Do not run dependent tasks"
)
@click.option("--view-tasks", is_flag=True, default=None, help="View task commands")
@click.option("--version", "-v", is_flag=True, default=None, help="Show rush version")
@click.argument("filter_names", required=False, nargs=-1)
def entrypoint(
    *,
    filter_names,
    all,
    hide_outputs,
    ignore_errors,
    path,
    no_deps,
    version,
    view_tasks,
):
    """A Minimalistic Bash Task Runner"""

    if len(sys.argv) == 1:
        entrypoint.main(["-h"])

    elif all and not filter_names and not view_tasks:
        run_tasks_obj = RunTasks(
            show_outputs=hide_outputs, catch_errors=ignore_errors, no_deps=no_deps
        )
        run_tasks_obj.run_all_tasks()

    elif filter_names and not view_tasks:
        run_tasks_obj = RunTasks(
            *filter_names,
            show_outputs=hide_outputs,
            catch_errors=ignore_errors,
            no_deps=no_deps,
        )
        run_tasks_obj.run_all_tasks()

    elif path:
        views_obj = Views()
        views_obj.view_rushpath

    elif view_tasks:
        views_obj = Views(*filter_names)
        views_obj.view_tasks

    elif version:
        click.secho(f"Rush version: {VERSION}", fg="green")
