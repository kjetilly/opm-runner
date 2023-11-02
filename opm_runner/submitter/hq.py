from .submitter import Submitter
import subprocess
import re


class HQ(Submitter):
    def __init__(self):
        self._jobs = []

    def __call__(self, cmd, *, stdoutfile, stderrfile):
        hqcmd = [
            'hq', 
            'submit',
            '--stdout',
            stdoutfile,
            '--stderr',
            stderrfile,
            *cmd
        ]

        runresult = subprocess.run(hqcmd, check=True, capture_output=True)
        jobid = re.search(r'Job submitted successfully, job ID: ([0-9]+)', runresult).group(1)
        self._jobs.append(jobid)

    
    def waitall(self):
        for id in self._jobs:
            subprocess.run(['hq', 'job', 'wait', id], check=True)

        return True
        
