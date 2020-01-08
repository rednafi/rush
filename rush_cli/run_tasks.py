from rush_cli.prep_tasks import PrepTasks
from rush_cli.utils import beautify_skiptask_name, run_task, scream


class RunTasks(PrepTasks):
    """Class for running the cleaned, flattened & filtered tasks."""

    def __init__(
        self, *filter_names, show_outputs=True, catch_errors=True, no_deps=False
    ):
        self.show_outputs = show_outputs
        self.catch_errors = catch_errors
        self.no_deps = no_deps
        super().__init__(no_deps=self.no_deps, *filter_names)

    def run_all_tasks(self):
        cleaned_tasks = self.get_prepared_tasks()
        scream(what="run")
        for task_name, task_chunk in cleaned_tasks.items():

            if not task_name.startswith("//"):
                run_task(
                    task_chunk,
                    task_name,
                    interactive=self.show_outputs,
                    catch_errors=self.catch_errors,
                )
            else:
                beautify_skiptask_name(task_name)
