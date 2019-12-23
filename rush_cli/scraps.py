import os
import click
import sys
import yaml


def _check_rushfiles():
    rushfiles = []
    for file in os.listdir("./"):
        if file.startswith("rushfile") and (
            file.endswith(".yml") or file.endswith(".yaml")
        ):
            rushfiles.append(file)
    return rushfiles


def _read_yml():
    rushfiles = _check_rushfiles()

    if len(rushfiles) < 1:
        sys.exit(
            click.style(
                "Error: Rushfile [rushfile.yml/rushfile.yaml] not found.", fg="magenta"
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

    try:
        rushfile = rushfiles[0]

        if rushfile.endswith(".yml"):
            with open("./rushfile.yml") as file:
                yml_content = yaml.load(file, Loader=yaml.FullLoader)
            return yml_content

        elif rushfile.endswith(".yaml"):
            with open("./rushfile.yaml") as file:
                yml_content = yaml.load(file, Loader=yaml.FullLoader)
            return yml_content

    except yaml.scanner.ScannerError:
        sys.exit(
            click.style("Error: rushfile.yml is not properly formatted", fg="magenta")
        )


rushfile = _check_rushfiles()[0]
if rushfile.endswith(".yaml"):
    with open("./rushfile.yaml") as file:
        yml_content = yaml.load(file, Loader=yaml.FullLoader)
print(yml_content)
