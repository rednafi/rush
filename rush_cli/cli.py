import click
import colorama
from click_help_colors import HelpColorsCommand

from rush_cli.run_tasks import RunTasks

# Don't strip colors.
colorama.init(strip=False)

VERSION = "0.3.4"


@click.command(
    context_settings=dict(
        help_option_names=["-h", "--help"], token_normalize_func=lambda x: x.lower()
    ),
    cls=HelpColorsCommand,
    help_headers_color="yellow",
    help_options_color="green",
)
@click.option(
    "--hide-outputs",
    is_flag=True,
    default=True,
    help="Option to hide interactive output.",
)
@click.option(
    "--hide-commands",
    is_flag=True,
    default=True,
    help="Option to disable printing commands.",
)
@click.option(
    "--ignore-errors", is_flag=True, default=True, help="Option to ignore errors."
)
@click.option("--view-tasks", is_flag=True, default=False, help="Option to view tasks.")
@click.option("--version", is_flag=True, default=False, help="Show rush version.")
@click.argument("filter_names", required=False, nargs=-1)
def entrypoint(
    *, filter_names, hide_outputs, hide_commands, ignore_errors, view_tasks, version
):
    """A Minimalistic Bash Task Runner"""
    if not version:
        run_tasks_obj = RunTasks(
            *filter_names,
            show_outputs=hide_outputs,
            show_commands=hide_commands,
            catch_errors=ignore_errors,
            view_tasks=view_tasks,
        )
        run_tasks_obj.run_all_tasks()

    else:
        version = VERSION
        click.secho(f"Rush version: {version}", fg="green")
