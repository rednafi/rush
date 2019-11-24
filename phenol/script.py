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
            job_list = split_lines(job_value)
            clean_commands[job_name] = job_list

        return clean_commands


class RunJobs(PreprocessJobs):

    def _unravel_commands(self):
        cmd = self.clean_commands()
        job_names = cmd.keys()
        job_values = cmd.values()

        unraveled_job_values = []

        for job_name, job_list in cmd.items():
            for job_line in job_list:
                if job_line in job_names:
                    job_line = cmd[job_line]
                unraveled_job_values.append(job_line)
            cmd[job_name] = unraveled_job_values
        return cmd

    def run_commands(self):
        cmd = self._unravel_commands()

        print(cmd)
        
obj = RunJobs()
obj.run_commands()
# subprocess.run(args='echo "hi"', shell=True)
