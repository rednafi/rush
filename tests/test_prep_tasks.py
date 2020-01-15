import os

import pytest

from rush_cli.prep_tasks import PrepTasks
from collections import OrderedDict


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
