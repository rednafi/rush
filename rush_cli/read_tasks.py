import os
import sys

import click
import pretty_errors
import yaml

from rush_cli.utils import find_shell_path


class ReadTasks:
    """Class for preprocessing tasks before running."""

    def __init__(self, *filter_names):
        self.use_shell = find_shell_path("bash")
        self.filter_names = filter_names

    def _check_rushfiles(self):
        """Check if there are multiple rushfiles in the same directory."""

        rushfiles = []
        for file in os.listdir("./"):
            if file.startswith("rushfile") and (
                file.endswith(".yml") or file.endswith(".yaml")
            ):
                rushfiles.append(file)

        if len(rushfiles) < 1:
            sys.exit(
                click.style(
                    "Error: Rushfile [rushfile.yml/rushfile.yaml] not found.",
                    fg="magenta",
                )
            )
        elif len(rushfiles) > 1:
            sys.exit(
                click.style(
                    "Error: Multiple rushfiles [rushfile.yml/rushfile.yaml]"
                    " in the same directory.",
                    fg="magenta",
                )
            )
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
            sys.exit(
                click.style(
                    "Error: rushfile.yml is not properly formatted", fg="magenta"
                )
            )
