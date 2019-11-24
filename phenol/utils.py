import subprocess


def strip_spaces(st):
    return st.rstrip()


def split_lines(st):
    return st.split("\n")


def echo_underlines(st):
    underline_len = len(st) + 3
    underlines = "=" * underline_len
    subprocess.run(f"echo '\n{st}:\n{underlines}'", shell=True)
