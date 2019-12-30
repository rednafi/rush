import os
import subprocess
import sys

import click
from invoke import run


def strip_spaces(st):
    return st.rstrip()


def split_lines(st):
    return st.split("\n")


def remove_comments(task_chunk: list) -> list:
    task_chunk = [task for task in task_chunk if not task.startswith("#")]
    return task_chunk


def beautify_task_name(task_name):
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
    click.echo(task_name)
    click.echo("")


def beautify_cmd(cmd):
    if not cmd.startswith("#"):
        separator = "=>"
        cmd = str(click.style(cmd, fg="cyan"))
        separator = str(click.style(separator, fg="cyan"))
        click.echo(f"{separator} {cmd}")


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


def run_task(cmd, cmd_name, interactive=True, catch_error=True):
    use_shell = find_shell_path()
    result = run(cmd, shell=use_shell, hide=True, warn=False)

    click.secho(f" {cmd_name}:", fg='yellow')
    click.secho(f" {'='*len(cmd_name)}", fg='green')

    if interactive:
        for line in result.stdout.splitlines():
            click.echo("  | " + line)
        if not catch_error:
            for line in result.stderr.splitlines():
                click.secho("  | " + line, fg='magenta')
        else:
            for line in result.stderr.splitlines():
                click.secho("  | " + line, fg='magenta')
                click.echo('err')
                sys.exit(1)

cmd = """ls -a | grep git
sudo l
echo 'hello'
"""
print(run_task(cmd, "task_1", interactive=False))
# result = run(cmd, shell=find_shell_path(), hide=True, warn=True)
# print(result.exited)
