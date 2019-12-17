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


def run_task(commands, interactive=True):

    std_out = sys.stdout if interactive else subprocess.PIPE
    std_in = sys.stdin if interactive else subprocess.PIPE

    process = subprocess.Popen(
        commands,
        stdout=std_out,
        stdin=std_in,
        universal_newlines=True,
        shell=True,
    )
    process.wait()


def system_which(command, mult=False):
    """Emulates the system's which. Returns None if not found."""
    _which = "which -a" if not os.name == "nt" else "where"
    # os.environ = {
    #     vistir.compat.fs_str(k): vistir.compat.fs_str(val)
    #     for k, val in os.environ.items()
    # }
    result = None
    try:
        c = delegator.run("{0} {1}".format(_which, command))
        try:
            # Which Not found…
            if c.return_code == 127:
                click.echo(
                    "{}: the {} system utility is required for bake to find bash properly."
                    "\n  Please install it.".format(
                        click.style("Warning", bold=True), click.style(_which, fg="red")
                    ),
                    err=True,
                )
            assert c.return_code == 0
        except AssertionError:
            result = None
    except TypeError:
        if not result:
            result = None
    else:
        if not result:
            result = next(iter([c.out, c.err]), "").split("\n")
            result = next(iter(result)) if not mult else result
            return result
        if not result:
            result = None
    result = [result] if mult else result
    return result
