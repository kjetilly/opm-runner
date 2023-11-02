from .submitter import Submitter
import subprocess


class Bash(Submitter):
    def __call__(self, *args, stderrfile=None, stdoutfile=None, **kwargs):
        with open(stderrfile, 'w') as err:
            with open(stdoutfile, 'w') as out:
                return subprocess.run(*args, check=True, stdout=out, stderr=err)
    
    def waitall(self):
        return True
