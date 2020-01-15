import os

import pytest
import yaml
from mock import patch
from rush_cli.read_tasks import ReadTasks


@pytest.fixture
def make_tmpdir(tmpdir):
    tmp_dir = tmpdir.mkdir("data")
    tmp_path = tmp_dir.join("rushfile.yml")

    return tmp_dir, tmp_path


@pytest.fixture
def make_cwd(request, make_tmpdir):
    tmp_dir, tmp_path = make_tmpdir
    patched = patch("os.getcwd", return_value=tmp_dir)
    request.addfinalizer(lambda: patched.__exit__())
    return patched.__enter__()


@pytest.fixture
def make_readtasks(make_cwd):
    """Initializing ReadTasks class."""

    obj = ReadTasks(
        use_shell="/bin/bash", filename="rushfile.yml", current_dir=os.getcwd()
    )
    return obj


# find_rushfile
@pytest.fixture
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


def test_init(make_readtasks):
    obj = make_readtasks
    assert obj.use_shell == "/bin/bash"
    assert obj.filename == "rushfile.yml"


# find_rushfile
def test_find_rushfile(make_readtasks, make_rushfile, make_tmpdir):
    obj = make_readtasks
    tmp_dir, tmp_path = make_tmpdir
    assert tmp_path == obj.find_rushfile()


# read_rushfile
def test_read_rushfile(make_readtasks, make_rushfile):
    obj = make_readtasks
    cont = make_rushfile
    assert cont == obj.read_rushfile()
