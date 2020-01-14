import os, click, sys
from rush_cli.utils import walk_up


def find_rushfile(filename, root=os.getcwd(), max_depth=4, topdown=False):
    """Returns the path of a rushfile in parent directories."""

    i = 0
    for c, d, f in walk_up(root):
        if i > max_depth:
            break
        elif filename in f:
            return os.path.join(c, filename)
        i += 1

    click.secho("Error: rushfile.yml not found.", fg="magenta")
    sys.exit(1)


print(find_rushfile('rushfile.yml', root='/home/redowan/code/rush'))
