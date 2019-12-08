import click

# + Executing random/entrypoints:

import sys

import colorama
import click

# Don't strip colors.
colorama.init(strip=False)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--read-stderr", is_flag=True, type=click.BOOL, default=True, help="Read stderr."
)
@click.option(
    "--no-color", is_flag=True, type=click.BOOL, default=False, help="Read stderr."
)
@click.option(
    "--color", nargs=1, type=click.STRING, default="green", help="Color to use."
)
@click.option("--char", nargs=1, type=click.STRING, default="--", help="Prefix char.")
def entrypoint1(*, char, read_stderr, no_color, color):
    """Indents and echoes string with a specific pipe."""

    pipe = sys.stdin if not read_stderr else sys.stderr

    if no_color:
        color = "white"

    for line in pipe:
        if line:
            title = str(click.style(line, fg=color))
            print(f" {char} ", end="")
            print(title.rstrip())
        else:
            print(f" {char} ", end="")

import subprocess
m = entrypoint1()
subprocess.run(m)
