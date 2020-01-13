import networkx as nx
from rush_cli.read_tasks import ReadTasks
from rush_cli.utils import scream, beautify_task_name, beautify_task_cmd
from pprint import pprint
import click
import matplotlib.pyplot as plt


class DepTasks(ReadTasks):
    """Class for listing and graphing dependent tasks."""

    def __init__(self, *filter_names):
        super().__init__(*filter_names)
        self.filter_names = filter_names

    def _prep_deps(self):
        """Preparing a dependency dict from yml contents."""

        # reading raw rushfile as a dict
        yml_content = self.read_rushfile()

        # splitting dict values by newlines
        yml_content = {k: v.split("\n") for k, v in yml_content.items() if v}

        # finding task dependencies
        deps = {}
        for k, v in yml_content.items():
            lst = []
            for cmd in v:
                if cmd in yml_content.keys():
                    lst.append(cmd)
            deps[k] = lst

        return deps

    def task_list(self):
        deps = self._prep_deps()

        scream(what="list")
        click.echo()
        for k, v in deps.items():
            click.secho(" " + "-" + " " + k, fg="yellow")
            for cmd in v:
                click.echo(" " * 4 + "-" + " " + cmd)

    def task_deps(self):
        """Drawing dependency graph."""

        deps = self._prep_deps()

        G = nx.OrderedDiGraph()
        G.add_nodes_from(deps.keys())
        G.add_edges_from([(k, cmd) for k, v in deps.items() for cmd in v])

        print(G.nodes)
        print(G.edges)

        # return nodes, edges


obj = DepTasks()
obj.task_deps()


# G = nx.DiGraph()
# G.add_nodes_from(
#     ["task_1", "task_2", "task_3", "//task_4", "task_5", "task_6", "task_7"]
# )
# G.add_edges_from([(1,2), (2,3)])
