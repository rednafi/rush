import yaml
import os
import subprocess
from typing import Dict, List
from utils import strip_spaces, split_lines, echo_underlines, run_task


class PreprocessTasks:
    def __init__(self):
        self.cleaned_tasks = {}
        self.ref_tasks = []


    def _read_yml(self) -> Dict[str, str]:
        """Read rushfile.yml file."""

        if os.path.exists("rushfile.yml"):
            with open("./rushfile.yml") as file:
                yml_content = yaml.load(file, Loader=yaml.FullLoader)
            return yml_content

        else:
            raise FileNotFoundError("rushfile.yml file not found")

    def _clean_tasks(self) -> Dict[str, List[str]]:
        """Clean spaces and split the commands by line."""

        yml_content = self._read_yml()

        for task_name, task_chunk in yml_content.items():
            task_chunk = strip_spaces(task_chunk)
            task_chunk = split_lines(task_chunk)
            self.cleaned_tasks[task_name] = task_chunk

        return self.cleaned_tasks


    # def add_reference_task(self):
    #     cleaned_tasks = self._clean_tasks()
    #     for k, v in cleaned_tasks.items():
    #         for line in v:
    #             if line == k:
    #                 self.ref_tasks.append(cleaned_tasks[line])

    #             elif line != k:
    #                 self.ref_tasks.append(line)

    #             else:
    #                 pass

    #     cleaned_tasks[k] = self.ref_tasks
    #     return cleaned_tasks


class RunTasks(PreprocessTasks):
    def __init__(self, *filter_names):
        super().__init__()
        self.tasks = self.add_reference_task
        self.filter_names = filter_names

    def filter_tasks(self):
        """Filtering out tasks by their tasknames for execution."""

        if self.filter_names:
            try:
                self.tasks = {
                    key: val
                    for key, val in self.tasks.items()
                    if key in self.filter_names
                }
                return self.tasks

            except KeyError:
                raise

    def exec(self):
        filtered_tasks = self.filter_tasks()

        for task_name, task_chunk in filtered_tasks.items():
            echo_underlines(task_name)

            for task_lines in task_chunk:
                if isinstance(task_lines, str):
                    run_task(task_lines)
                else:
                    for task_line in task_lines:
                        run_task(task_line)


from pprint import pprint

obj = PreprocessTasks()
pprint(obj.add_reference_task())
print("")
