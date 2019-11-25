import click
from .script import RunTasks


@click.command()
@click.option("--help", default=1, help="run rush taskname")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo("Hello %s!" % name)
