import subprocess
import sys
import time
import os
import click


def strip_spaces(st):
    return st.rstrip()


def split_lines(st):
    return st.split("\n")


def check_shell():
    try:
        sub = subprocess.check_output(["which", "-a", "bash"], universal_newlines=True)
        output = sub.split("\n")
        if "/bin/bash" in output:
            return "/bin/bash"
        if "/usr/bin/bash" in output:
            return "/usr/bin/bash"

    except subprocess.CalledProcessError:
        click.echo(
            click.style("No shell found. You need a shell to use Rush.", fg="red")
        )
        sys.exit()


def run_task(use_shell, command, capture_err=True):

    if capture_err:
        proc = subprocess.check_output(
            [use_shell, "-c", command], universal_newlines=True
        )
        click.echo(proc)
    else:
        proc = subprocess.run(
            [use_shell, "-c", command], universal_newlines=True, capture_output=True
        ).stdout
        click.echo(proc)
