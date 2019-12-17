import subprocess
import sys
import time
import os
import delegator
import click


def strip_spaces(st):
    return st.rstrip()


def split_lines(st):
    return st.split("\n")


def run_task(command, capture_error=True):

    # std_out = sys.stdout if interactive else subprocess.PIPE
    # std_in = sys.stdin if interactive else subprocess.PIPE

    if capture_error:
        proc = subprocess.check_output(command, universal_newlines=True, shell=True)
        click.echo(proc)
    else:
        proc = subprocess.run(
            command, universal_newlines=True, capture_output=True, shell=True
        ).stdout
        click.echo(proc)

