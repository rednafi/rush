from rush_cli.prep_tasks import PrepTasks
from rush_cli.utils import beautify_skiptask_name, run_task


class RunTasks(PrepTasks):
    """Class for running the cleaned, flattened & filtered tasks."""

    def __init__(self, *filter_names, show_outputs=True, catch_errors=True):
        super().__init__(*filter_names)
        self.show_outputs = show_outputs
        self.catch_errors = catch_errors
        self.cleaned_tasks = self.get_prepared_tasks()

    def run_all_tasks(self):
        for task_name, task_chunk in self.cleaned_tasks.items():
            if not task_name.startswith("//"):
                run_task(
                    task_chunk,
                    task_name,
                    interactive=self.show_outputs,
                    catch_errors=self.catch_errors,
                )
            else:
                beautify_skiptask_name(task_name)
