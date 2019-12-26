import click
import colorama

from rush_cli.run_tasks import RunTasks

# Don't strip colors.
colorama.init(strip=False)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--interactive/--not-interactive",
    default=True,
    help="Option to show/hide interactive output.",
)
@click.option("--color/--no-color", default=True, help="Option enable/disable colors.")
@click.option(
    "--print-cmd/--not-print-cmd",
    default=True,
    help="Option to enable/disable printing commands.",
)
@click.option(
    "--capture-err/--ignore-err", default=True, help="Option to capture/ignore errors."
)
@click.argument("filter_names", required=False, nargs=-1)
def entrypoint(*, filter_names, interactive, color, print_cmd, capture_err):
    run_tasks_obj = RunTasks(
        *filter_names,
        interactive=interactive,
        is_color=color,
        print_cmd=print_cmd,
        capture_err=capture_err
    )
    run_tasks_obj.run_all_tasks()
