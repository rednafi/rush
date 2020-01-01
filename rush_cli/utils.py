import os
import subprocess
import sys

import click


def strip_spaces(st):
    return st.rstrip()


def split_lines(st):
    return st.split("\n")


def beautify_task_name(task_name):
    click.echo("")
    task_name = f"{task_name}:"
    underline_len = len(task_name) + 3
    underline = "=" * underline_len

    task_name = str(click.style(task_name, fg="yellow"))
    underline = str(click.style(underline, fg="green"))

    click.echo(task_name)
    click.echo(underline)


def beautify_skiptask_name(task_name):
    task_name = f"=> Ignoring task {task_name}"
    task_name = click.style(task_name, fg="blue")
    click.echo("")
    click.echo(task_name)


def find_shell_path(shell_name="bash"):
    """Finds out system's bash interpreter path"""

    if not os.name == "nt":
        cmd = ["which", "-a", shell_name]
    else:
        cmd = ["where", shell_name]

    try:
        c = subprocess.run(
            cmd, universal_newlines=True, check=True, capture_output=True
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
