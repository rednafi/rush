# import os
# import delegator
# import click
# import subprocess
# import sys


# def find_shell_path(shell_name):
#     """Finds out system's bash interpreter path"""

#     if not os.name == "nt":
#         cmd = ["which", "-a", shell_name]
#     else:
#         cmd = ["where", shell_name]

#     try:
#         c = subprocess.run(
#             cmd, universal_newlines=True, check=True, capture_output=True
#         )
#         output = c.stdout.split("\n")
#         output = [_ for _ in output if _]

#         _shell_paths = [f"/bin/{shell_name}", f"/usr/bin/{shell_name}"]

#         for path in output:
#             if path == _shell_paths[0]:
#                 return path
#             elif path == _shell_paths[1]:
#                 return path

#     except subprocess.CalledProcessError:
#         click.echo(
#             click.style("No shell found. You need a shell to use Rush.", fg="red")
#         )
#         sys.exit(1)


# print(find_shell_path("fish"))
