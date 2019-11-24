import yaml
import os
import subprocess
from utils import strip_spaces, split_lines, echo_underlines


class PreprocessJobs:
    def _read_yml(self):
        """Read phenol.yml file."""

        if os.path.exists("phenol.yml"):
            with open("./phenol.yml") as file:
                yml_content = yaml.load(file, Loader=yaml.FullLoader)
            return yml_content

        else:
            raise FileNotFoundError("phenol.yml file not found")

    def clean_commands(self):
        """Clean spaces and split the commands by line."""

        yml_content = self._read_yml()

        clean_commands = {}
        for job_name, job_value in yml_content.items():
            job_value = strip_spaces(job_value)
            cmd_list = split_lines(job_value)
            clean_commands[job_name] = cmd_list

        return clean_commands


class RunJobs(PreprocessJobs):
    def run_commands(self):
        cmd = self.clean_commands()

        for job_name, job_value in cmd.items():
            echo_underlines(job_name)
            for line in job_value:
                if not line == job_name:
                    val ==

                else:
                    subprocess.run(line, shell=True)


obj = RunJobs()
obj.run_commands()
# subprocess.run(args='echo "hi"', shell=True)
