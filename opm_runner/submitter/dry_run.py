from .submitter import Submitter
import subprocess


class DryRun(Submitter):
    def __call__(self, *args, stderrfile=None, stdoutfile=None, **kwargs):
        print(f"Would run\n\t{' '.join(args)}")
    
    def waitall(self):
        return True
