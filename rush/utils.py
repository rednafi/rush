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


def run_task(command, interactive=True, capture_error=True):

    std_out = sys.stdout if interactive else subprocess.PIPE
    std_in = sys.stdin if interactive else subprocess.PIPE

    if interactive and capture_error:
        proc = subprocess.check_output(command, universal_newlines=True, shell=True)
        print(proc)
    else:
        subprocess.run(
            command, stdout=std_out, stdin=std_in, universal_newlines=True, shell=True
        )

#run_task('eco "hi"')
