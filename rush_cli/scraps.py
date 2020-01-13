import networkx as nx
from rush_cli.read_tasks import ReadTasks
from pprint import pprint

obj = ReadTasks()

# reading raw rushfile as a dict
yml_content = obj.read_rushfile()

# splitting dict values by newlines
yml_content = {k: v.split("\n") for k, v in yml_content.items() if v}

# removing commented out task names
yml_content = {k.replace("//", ""): v for k, v in yml_content.items()}

# finding task dependencies

task_deps = {}
for k, v in yml_content.items():
    lst = []
    for cmd in v:
        if cmd in yml_content.keys():
            lst.append(cmd)
    task_deps[k] = lst



G = nx.DiGraph()
for k, v in task_deps.items():
    G.add_node(k)
    for cmd in v:
        G.add_edge(k, cmd)

print(G.nodes())
print(G.edges())
print(list(nx.dfs_edges(G, source='task_7')))
