# RUSH
~~ A Minimalistic Shell-Task Runner ~~

Run all your task automation shell commands from a single `rushfile.yml` file.

## Installation

```
$ pip install rush-cli
```

## Workflow

Here is a rushfile. It needs to reside in the root directory:

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

* Run all tasks
    ```
    $ rush
    ```

* Run specific tasks
    ```
    $ rush task_1 task_4
    ```

* Run tasks while hiding individual commands
    ```
    $ rush task_1 task_2 --not-print-cmd
    ```

* Run tasks ignoring errors
    ```
    $ rush --not-capture-err
    ```

## Quirks

* Rush runs all the commands using `/bin/sh` (not bash or anything else). So shell specific scripts might throw error.

* Currently task chaining is not supported. 
