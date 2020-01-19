import os

import pytest

from rush_cli.prep_tasks import PrepTasks, Views
from collections import OrderedDict
from mock import patch
import yaml


@pytest.fixture
def make_preptasks():
    obj = PrepTasks()

    return obj


def test_clean_tasks(make_preptasks):
    obj = make_preptasks

    assert obj._clean_tasks(
        {
            "task_1": 'echo "task1 is running"\n',
            "task_2": 'task_1\necho "task2 is running"\n',
        }
    ) == OrderedDict(
        [
            ("task_1", ['echo "task1 is running"']),
            ("task_2", ["task_1", 'echo "task2 is running"']),
        ]
    )


def test_replace_placeholder_tasks(make_preptasks):
    obj = make_preptasks

    assert obj._replace_placeholder_tasks(
        ["task_1", 'echo "task"'], {"task_1": "hello"}
    ) == ["hello", 'echo "task"']


def test_flatten_task_chunk(make_preptasks):
    obj = make_preptasks

    assert obj._flatten_task_chunk(
        [["hello"], ["from", ["the", ["other"]], "side"]]
    ) == ["hello", "from", "the", "other", "side"]


def test_filter_tasks(make_preptasks):
    obj = make_preptasks

    assert obj._filter_tasks(
        {"task_1": "ay", "task_2": "g", "task_3": "homie"}, "task_1", "task_3"
    ) == {"task_1": "ay", "task_3": "homie"}

    with pytest.raises(SystemExit):
        obj._filter_tasks(
            {"task_1": "ay", "task_2": "g", "task_3": "homie"}, "task_1", "task_4"
        )


@pytest.fixture(autouse=True)
def make_tmpdir(tmpdir):
    tmp_dir = tmpdir.mkdir("folder")
    tmp_path = tmp_dir.join("rushfile.yml")

    return tmp_dir, tmp_path


@pytest.fixture(autouse=True)
def make_cwd(request, make_tmpdir):
    tmp_dir, tmp_path = make_tmpdir
    patched = patch("os.getcwd", return_value=tmp_dir)
    request.addfinalizer(lambda: patched.__exit__())
    return patched.__enter__()


# find_rushfile
@pytest.fixture(autouse=True)
def make_rushfile(make_tmpdir):
    """Creating dummy rushfile.yml."""

    # dummy rushfile path
    tmp_dir, tmp_path = make_tmpdir

    # dummy rushfile contents
    content = """task_1: |
    echo "task1 is running"

    task_2: |
        # Task chaining [task_1 is a dependency of task_2]
        task_1
        echo "task2 is running"
    """

    # loading dummy rushfile
    yml_content = yaml.load(content, Loader=yaml.FullLoader)

    # saving dummy rushfile to tmp dir
    with open(tmp_path, "w") as f:
        yaml.dump(yml_content, f)

    return yml_content


@pytest.fixture
def make_views():
    obj = Views()
    return obj


def test_view_rushpath(capsys, make_views):
    obj = make_views
    obj.view_rushpath
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out.rstrip().split("/")[-1] == "rushfile.yml"
