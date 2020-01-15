import pytest

from rush_cli.utils import (
    walk_up,
    beautify_task_name,
    beautify_task_name,
    beautify_skiptask_name,
    beautify_task_cmd,
    scream,
    find_shell_path
)

from click.testing import CliRunner


@pytest.fixture(autouse=True)
def make_tmpdir(tmpdir):
    tmp_dir = tmpdir.mkdir("faka")
    return str(tmp_dir)


def test_walk_up(make_tmpdir):
    dirs = list(walk_up(make_tmpdir))
    assert isinstance(dirs[0][0], str)
    assert dirs[0][0].split("/")[-1] == "faka"
    assert dirs[0][1] == []
    assert dirs[0][2] == []


def test_beautify_task_name(capsys):

    beautify_task_name("task_1")
    captured = capsys.readouterr()
    assert captured.out == "\ntask_1:\n==========\n"


def test_beautify_skiptask_name(capsys):
    beautify_skiptask_name("task_4")
    captured = capsys.readouterr()
    assert captured.out == "\n=> Ignoring task task_4\n"


def test_beautify_task_cmd(capsys):
    beautify_task_cmd("echo 'hello'")
    captured = capsys.readouterr()
    assert captured.out == "echo 'hello'\n"


def test_scream(capsys):
    scream("run")
    captured = capsys.readouterr()
    assert captured.out == "\nRUNNING TASKS...\n------------------\n"

    scream("view")
    captured = capsys.readouterr()
    assert captured.out == "\nVIEWING TASKS...\n------------------\n"

    scream("list")
    captured = capsys.readouterr()
    assert captured.out == "\nTASK LIST...\n------------------\n"

