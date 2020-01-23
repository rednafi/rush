import os
import subprocess
import sys

import click
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import BashLexer


def walk_up(bottom):
    """mimic os.walk, but walk 'up' instead of down the directory tree.
    From: https://gist.github.com/zdavkeos/1098474
    """

    bottom = os.path.realpath(bottom)

    # get files in current dir
    try:
        names = os.listdir(bottom)
    except Exception:
        return

    dirs, nondirs = [], []
    for name in names:
        if os.path.isdir(os.path.join(bottom, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    yield bottom, dirs, nondirs

    new_path = os.path.realpath(os.path.join(bottom, ".."))

    # see if we are at the top
    if new_path == bottom:
        return

    for x in walk_up(new_path):
        yield x


def check_pipe(yml_content, no_warns=False):
    """Check if there is a pipe ('|') after each task name.
    Raise exception if pipe is missing."""

    for task_name, task_chunk in yml_content.items():
        if task_chunk:
            if not task_chunk.endswith("\n") and not no_warns:
                click.secho(
                    f"Warning: Pipe (|) after {task_name} is missing", fg="yellow"
                )


def beautify_task_name(task_name):
    click.echo()
    task_name = f"{task_name}:"
    underline_len = len(task_name) + 3
    underline = "=" * underline_len

    task_name = str(click.style(task_name, fg="yellow"))
    underline = str(click.style(underline, fg="green"))

    click.echo(task_name)
    click.echo(underline)


def beautify_skiptask_name(task_name):
    task_name = f"=> Ignoring task {task_name}"
    task_name = click.style(task_name, fg="cyan")
    click.echo("")
    click.echo(task_name)


def beautify_task_cmd(cmd: str):
    """Highlighting the bash commands."""

    cmd = highlight(cmd, BashLexer(), TerminalFormatter())
    cmd = cmd.rstrip()
    click.echo(cmd)


def scream(what):
    """Screaming 'Viewing Tasks'... or 'Running Tasks'."""

    separator = "-" * 18

    if what == "run":
        click.echo()
        click.secho("RUNNING TASKS...", fg="green", bold=True)
        click.secho(separator)

    elif what == "view":
        click.echo()
        click.secho("VIEWING TASKS...", fg="green", bold=True)
        click.secho(separator)

    elif what == "list":
        click.echo()
        click.secho("TASK LIST...", fg="green", bold=True)
        click.secho(separator)

    elif what == "dep":
        click.echo()
        click.secho("TASK DEPENDENCIES...", fg="green", bold=True)
        click.secho(separator)


def find_shell_path(shell_name="bash"):
    """Finds out system's bash interpreter path."""

    if not os.name == "nt":
        cmd = ["which", "-a", shell_name]
    else:
        cmd = ["where", shell_name]

    try:
        c = subprocess.run(
            cmd,
            universal_newlines=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output = c.stdout.split("\n")
        output = [_ for _ in output if _]

        for path in output:
            if path == f"/bin/{shell_name}":
                return path

    except subprocess.CalledProcessError:
        click.secho("Error: Bash not found. Install Bash to use Rush.", fg="magenta")
        sys.exit(1)


def run_task(task: str, task_name: str, interactive=True, catch_errors=True):
    """Primary function that runs a task chunk."""

    use_shell = find_shell_path()
    std_in = sys.stdin if interactive else subprocess.PIPE
    std_out = sys.stdout if interactive else subprocess.PIPE

    beautify_task_name(task_name)
    try:
        process = subprocess.run(
            [use_shell, "-c", task],
            stdin=std_in,
            stdout=std_out,
            universal_newlines=True,
            check=catch_errors,
        )
    except subprocess.CalledProcessError:
        click.secho("Error occured: Shutting down")
        sys.exit(1)
