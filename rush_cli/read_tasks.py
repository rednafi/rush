import os
import sys

import click
import yaml

from rush_cli.utils import find_shell_path, walk_up, check_pipe


class ReadTasks:
    """Class for preprocessing tasks before running."""

    def __init__(
        self,
        use_shell=find_shell_path("bash"),
        filename="rushfile.yml",
        current_dir=os.getcwd(),
        no_warns=False,
    ):
        self.use_shell = use_shell
        self.filename = filename
        self.current_dir = current_dir
        self.no_warns = no_warns

    def find_rushfile(self, max_depth=4, topdown=False):
        """Returns the path of a rushfile in parent directories."""

        i = 0
        for c, d, f in walk_up(self.current_dir):
            if i > max_depth:
                break
            elif self.filename in f:
                return os.path.join(c, self.filename)
            i += 1

        click.secho("Error: rushfile.yml not found.", fg="magenta")
        sys.exit(1)

    def read_rushfile(self):

        rushfile = self.find_rushfile()
        try:
            with open(rushfile) as file:
                yml_content = yaml.load(file, Loader=yaml.SafeLoader)

                # make sure the task names are strings
                yml_content = {str(k): v for k, v in yml_content.items()}

                # if pipe is missing then raise exception
                check_pipe(yml_content, no_warns=self.no_warns)

            return yml_content

        except (yaml.scanner.ScannerError, yaml.parser.ParserError):
            click.secho("Error: rushfile.yml is not properly formatted", fg="magenta")
            sys.exit(1)

        except AttributeError:
            click.secho("Error: rushfile.yml is empty", fg="magenta")
            sys.exit(1)


# from pprint import pprint

# obj = ReadTasks()
# pprint(obj.read_rushfile()["//task_4"])
