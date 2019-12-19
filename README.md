<div align="center">

# Rush
A Minimalistic Shell-Task Runner
</div>

Run all your task automation shell commands from a single `rushfile.yml` file.

## Features
* By default, runs commands in interactive mode
* Option to show or not-show individual commands in a task chunk as they get executed
* Option to highlight or not-highlight individual task names and task commands
* Option to catch or ignore command errors
* Command chaining is supported (See the example `rushfile.yml` where `task_2` is chained to `task_1`)

## Installation

```
$ pip install rush-cli
```

## Workflow

* Here is an example `rushfile.yml`. It needs to reside in the root directory:

    ``` yml
    task_1: |
        echo "task1 is running"
        ls

    task_2: |
        echo "task2 is running"

    task_3: |
        sudo -euo pipefail
        ls -a
        echo "task_3 subtask1 is running"

    task_4: |
        ls | grep cli
        ls > he.txt1
    ```

* See all the available options
    ```
    $ rush --help
    ```
    This should show:
    ```
    Usage: rush [OPTIONS] [FILTER_NAMES]...

    Options:
    --color / --no-color           Option to color the commands.
    --print-cmd / --not-print-cmd  Option to print the executing commands.
    --capture-err / --ignore-err   Option to capture errors
    -h, --help                     Show this message and exit.
    ```

* Run all tasks
    ```
    $ rush
    ```

* Run specific tasks
    ```
    $ rush task_1 task_4
    ```

* Run tasks without printing individual commands
    ```
    $ rush task_1 task_2 --not-print-cmd
    ```

* Run tasks ignoring errors
    ```
    $ rush --ignore-err
    ```

* Remove color
    ```
    $ rush --no-color
    ```


## Quirks

* Rush runs all the commands using `/bin/sh` (not bash or anything else). So shell specific scripts might throw error.
