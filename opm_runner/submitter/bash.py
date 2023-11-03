from .submitter import Submitter
import subprocess


class Bash(Submitter):
    def __call__(self, cli, stderrfile=None, stdoutfile=None, check=True):
        with open(stderrfile, "w") as err:
            with open(stdoutfile, "w") as out:
                return subprocess.run(cli, check=check, stdout=out, stderr=err)

    def waitall(self):
        return True
