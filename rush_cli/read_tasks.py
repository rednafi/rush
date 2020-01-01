import os
import sys

import click
import pretty_errors
import yaml

from rush_cli.utils import find_shell_path


class ReadTasks:
    """Class for preprocessing tasks before running."""

    def __init__(self):
        self.use_shell = find_shell_path("bash")

    def _check_rushfiles(self):
        """Check if there are multiple rushfiles in the same directory."""

        rushfiles = []
        current_path = os.listdir("./")

        if current_path:
            for file in current_path:
                filename = file.split(".")[0]
                extension = file.split(".")[-1]

                if filename == "rushfile" and (
                    extension == "yml" or extension == "yaml"
                ):
                    rushfiles.append(file)

        if len(rushfiles) < 1:
            click.secho(
                "Error: Rushfile [rushfile.yml/rushfile.yaml] not found.", fg="magenta"
            )
            sys.exit(1)
        elif len(rushfiles) > 1:
            click.secho(
                "Error: Multiple rushfiles" " in the same directory.", fg="magenta"
            )
            sys.exit(1)
        else:
            rushfile = rushfiles[0]
        return rushfile

    def read_yml(self):
        rushfile = self._check_rushfiles()
        try:
            if rushfile.endswith(".yml"):
                with open("./rushfile.yml") as file:
                    yml_content = yaml.load(file, Loader=yaml.FullLoader)
                    # make sure the task names are strings
                    yml_content = {str(k): v for k, v in yml_content.items()}
                return yml_content

            elif rushfile.endswith(".yaml"):
                with open("./rushfile.yaml") as file:
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
