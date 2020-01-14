import pytest
from rush_cli.read_tasks import ReadTasks
import yaml
from mock import patch
import os
import py


@pytest.fixture
def fix_tmpdir(tmpdir):
    tmp_dir = tmpdir.mkdir("data")
    tmp_path = tmp_dir.join("rushfile.yml")
    return str(tmp_dir), str(tmp_path)


@pytest.fixture(scope="function")
def fix_getcwd(request, fix_tmpdir):
    tmp_dir, tmp_path = fix_tmpdir
    patched = patch("os.getcwd", return_value=tmp_dir)
    request.addfinalizer(lambda: patched.__exit__())
    return patched.__enter__()


@pytest.fixture
def init_read_tasks(fix_getcwd):
    """Initializing ReadTasks class."""

    obj = ReadTasks(
        use_shell="/bin/bash", filename="rushfile.yml", current_dir=os.getcwd()
    )

    return obj


def test_init(init_read_tasks):
    obj = init_read_tasks
    assert obj.use_shell == "/bin/bash"
    assert obj.filename == "rushfile.yml"


# find_rushfile
@pytest.fixture(scope="function")
def fix_rushfile_content(fix_tmpdir):
    """Creating dummy rushfile.yml."""

    # dummy rushfile path
    tmp_dir, tmp_path = fix_tmpdir

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


# find_rushfile
def test_find_rushfile(init_read_tasks, fix_rushfile_content, fix_tmpdir):
    obj = init_read_tasks
    tmp_dir, tmp_path = fix_tmpdir
    assert tmp_path == obj.find_rushfile()


# read_rushfile
def test_read_rushfile(init_read_tasks, fix_rushfile_content):
    obj = init_read_tasks
    cont = fix_rushfile_content
    obj.read_rushfile()
    assert cont == obj.read_rushfile()
