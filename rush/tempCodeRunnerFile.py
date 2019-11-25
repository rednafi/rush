class RunTasks(PreprocessTasks):
#     def __init__(self, *filter_names):
#         super().__init__()
#         self.tasks = self.add_reference_task
#         self.filter_names = filter_names

#     @staticmethod
#     def unravel_tasks():
#         pass

#     def filter_tasks(self):
#         """Filtering out tasks by their tasknames for execution."""

#         if self.filter_names:
#             try:
#                 self.tasks = {
#                     key: val
#                     for key, val in self.tasks.items()
#                     if key in self.filter_names
#                 }
#                 return self.tasks

#             except KeyError:
#                 raise

#     def exec(self):
#         filtered_tasks = self.filter_tasks()

#         for task_name, task_chunk in filtered_tasks.items():
#             echo_underlines(task_name)

#             for task_lines in task_chunk:
#                 if isinstance(task_lines, str):
#                     run_task(task_lines)
#                 else:
#                     for task_line in task_lines:
#                         run_task(task_line)


# obj = RunTasks("job2", "job4")
# obj.exec()
