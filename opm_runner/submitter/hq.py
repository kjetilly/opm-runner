from .submitter import Submitter
import subprocess
import re
from tqdm import tqdm


class HQ(Submitter):
    def __init__(self):
        self._jobs = []

    def __call__(self, cmd, *, stdoutfile, stderrfile, check=True):
        hqcmd = ["hq", "submit", "--stdout", stdoutfile, "--stderr", stderrfile, *cmd]

        try:
            runresult = subprocess.run(hqcmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Trying to run the following command:\n\t{' '.join(hqcmd)}\nfailed.")
            raise e
        jobid = re.search(
            r"Job submitted successfully, job ID: ([0-9]+)",
            runresult.stdout.decode(),
        ).group(1)

        self._jobs.append(jobid)

    def waitall(self):
        failed = 0
        finished = 0
        with tqdm(self._jobs, desc="Waiting for samples to complete") as t:
            t.set_postfix(failed=failed, finished=finished)
            for id in t:
                try:
                    with open(f"hq_wait_log_{id}.txt", 'w') as logfile:
                        subprocess.run(
                            ["hq", "job", "wait", id],
                            check=True,
                            stderr=subprocess.STDOUT,
                            stdout=logfile,
                        )
                    finished += 1
                except subprocess.CalledProcessError:
                    failed += 1
                t.set_postfix(failed=failed, finished=finished)
        return True

    def runall(self, concurrent_samples, sample_runner, all_samples):
        for sample in tqdm(all_samples, desc="Submitting samples"):
            sample_runner(sample)
