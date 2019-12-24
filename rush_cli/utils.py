import subprocess
import sys
import click


def strip_spaces(st):
    return st.rstrip()


def split_lines(st):
    return st.split("\n")


def check_shell():
    try:
        sub = subprocess.check_output(["which", "-a", "sh"], universal_newlines=True)
        output = sub.split("\n")
        if "/bin/sh" in output:
            return "/bin/sh"
        if "/usr/bin/bash" in output:
            return "/usr/bin/sh"

    except subprocess.CalledProcessError:
        click.echo(
            click.style("No shell found. You need a shell to use Rush.", fg="red")
        )
        sys.exit()


def beautify_task_name(task_name, is_color=True):
    task_name = f"{task_name}:"
    underline_len = len(task_name) + 3
    underline = "=" * underline_len

    if is_color:
        task_name = str(click.style(task_name, fg="yellow"))
        underline = str(click.style(underline, fg="green"))

    click.echo(task_name)
    click.echo(underline)


def beautify_skiptask_name(task_name, is_color=True):
    task_name = f"=> Ignoring task {task_name}"
    if is_color:
        task_name = click.style(task_name, fg="blue")
    click.echo(task_name)


def beautify_cmd(cmd, is_color=True):
    separator = "=>"
    if is_color:
        cmd = str(click.style(cmd, fg="cyan"))
        separator = str(click.style(separator, fg="cyan"))
    click.echo(f"{separator} {cmd}")


def run_task(use_shell, command, interactive=True, capture_err=True):
    std_out = sys.stdout if interactive else subprocess.PIPE
    std_in = sys.stdin if interactive else subprocess.PIPE

    res = subprocess.run(
        [use_shell, "-c", command],
        stdout=std_out,
        stdin=std_in,
        stderr=std_out,
        universal_newlines=True,
        check=capture_err,
        capture_output=False,
    )
    click.echo("")
