import sys

import click
import colorama
from click_help_colors import HelpColorsCommand

from rush_cli.prep_tasks import Views
from rush_cli.run_tasks import RunTasks

# Don't strip colors.
colorama.init(strip=False)

VERSION = "0.3.9"


@click.command(
    context_settings=dict(
        help_option_names=["-h", "--help"], token_normalize_func=lambda x: x.lower()
    ),
    cls=HelpColorsCommand,
    help_headers_color="yellow",
    help_options_color="green",
)
@click.option(
    "--all", "-a", is_flag=True, default=False, multiple=True, help="Run all tasks."
)
@click.option(
    "--hide-outputs",
    is_flag=True,
    default=True,
    help="Option to hide interactive output.",
)
@click.option(
    "--ignore-errors", is_flag=True, default=True, help="Option to ignore errors."
)
@click.option("--path", is_flag=True, default=False, help="Show the absolute path of rushfile.yml")
@click.option("--version", is_flag=True, default=False, help="Show rush version.")

@click.argument("filter_names", required=False, nargs=-1)
def entrypoint(*, filter_names, all, hide_outputs, ignore_errors, path, version):
    """A Minimalistic Bash Task Runner"""

    if len(sys.argv) == 1:
        entrypoint.main(["-h"])

    elif all and not filter_names:
        run_tasks_obj = RunTasks(show_outputs=hide_outputs, catch_errors=ignore_errors)
        run_tasks_obj.run_all_tasks()

    elif filter_names:
        run_tasks_obj = RunTasks(
            *filter_names, show_outputs=hide_outputs, catch_errors=ignore_errors
        )
        run_tasks_obj.run_all_tasks()

    elif path:
        views_obj = Views()
        views_obj.view_rushpath

    elif version:
        click.secho(f"Rush version: {VERSION}", fg="green")
