import os
import sys

import click
import pretty_errors
import yaml

from rush_cli.utils import find_shell_path, walk_up


class ReadTasks:
    """Class for preprocessing tasks before running."""

    def __init__(self):
        self.use_shell = find_shell_path("bash")
        self.filename = "rushfile.yml"

    def find_rushfile(self, root=os.getcwd(), max_depth=4, topdown=False):
        """Returns the path of a rushfile in parent directories."""

        i = 0
        for c, d, f in walk_up(root):
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
                yml_content = yaml.load(file, Loader=yaml.FullLoader)
                # make sure the task names are strings
                yml_content = {str(k): v for k, v in yml_content.items()}
            return yml_content

        except (yaml.scanner.ScannerError, yaml.parser.ParserError):
            click.secho("Error: rushfile.yml is not properly formatted", fg="magenta")
            sys.exit(1)

        except AttributeError:
            click.secho("Error: rushfile.yml is empty", fg="magenta")
            sys.exit(1)
