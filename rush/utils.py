import subprocess


def strip_spaces(st):
    return st.rstrip()


def split_lines(st):
    return st.split("\n")


def echo_underlines(st):
    underline_len = len(st) + 5
    underlines = "=" * underline_len
    subprocess.run(f"echo '\n{st}:\n{underlines}'", shell=True)


def run_task(st):
    subprocess.run(st, shell=True)
