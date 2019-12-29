import click
import colorama

from rush_cli.run_tasks import RunTasks
from rush_cli.read_tasks import ViewTasks
from click_help_colors import HelpColorsCommand

# Don't strip colors.
colorama.init(strip=False)


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
    help="Option to show/hide interactive output.",
)
@click.option(
    "--hide-commands",
    is_flag=True,
    default=True,
    help="Option to enable/disable printing commands.",
)
@click.option(
    "--ignore-errors",
    is_flag=True,
    default=True,
    help="Option to capture/ignore errors.",
)
@click.option("--view-tasks", is_flag=True, default=False, help="View tasks")
@click.argument("filter_names", required=False, nargs=-1)
def entrypoint(*, filter_names, hide_outputs, hide_commands, ignore_errors, view_tasks):
    """A Minimalistic Bash Task Runner"""
    if not view_tasks:
        run_tasks_obj = RunTasks(
            
            *filter_names,
            show_outputs=hide_outputs,
            show_commands=hide_commands,
            catch_errors=ignore_errors,
        )
        run_tasks_obj.run_all_tasks()
    else:
        obj = ViewTasks()
        obj.view_tasks()
