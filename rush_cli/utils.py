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



def run_task(use_shell, command, interactive=True, capture_err=True):
    std_out = sys.stdout if interactive else subprocess.PIPE
    std_in = sys.stdin if interactive else subprocess.PIPE

    res = subprocess.run(
        [use_shell, "-c", command],
        stdout=std_out,
        stdin=std_in,
        stderr=std_out,
        universal_newlines=True,
    )
    click.echo("")

    # click.echo(res.stdout)
    # click.echo(res.stderr)


# print(run_task(check_shell(), "ls | grep cli"))
