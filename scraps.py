
import yaml

from pprint import pprint
from rush_cli.prep_tasks import PrepTasks

obj = PrepTasks()
cleaned_tasks = obj.get_prepared_tasks()



pprint(cleaned_tasks)
