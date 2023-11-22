from .submitter import Submitter
import subprocess
import re
from tqdm import tqdm
import threading


class HQ(Submitter):
    def __init__(self):
        self._jobs = []

        self._waitall_lock = threading.RLock()
        self._hq_waitall_lock = threading.RLock()

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

    def _wait_for_sample(self, id, progress_bar):
        try:
            with open(f"hq_wait_log_{id}.txt", 'w') as logfile:
                subprocess.run(
                    ["hq", "job", "wait", id],
                    check=True,
                    stderr=subprocess.STDOUT,
                    stdout=logfile,
                )
            with self._hq_waitall_lock:
                self._finished += 1
        except subprocess.CalledProcessError:
            with self._hq_waitall_lock:
                self._failed += 1
        with self._hq_waitall_lock:
            progress_bar.update(1)
            progress_bar.set_postfix(failed=self._failed, finished=self._finished)
            

    def waitall(self):
        # This function is not thread safe:
        with self._waitall_lock:
            self._failed = 0
            self._finished = 0
            
            with tqdm(total=len(self._jobs), desc="Waiting for samples to complete") as progress_bar:
                threads = []
                progress_bar.set_postfix(failed=self._failed, finished=self._finished)
                for id in self._jobs:
                    thread = threading.Thread(target=self._wait_for_sample, args=[id, progress_bar])
                    thread.run()
                    threads.append(thread)
                    
                for thread in threads:
                    thread.join()
            return True

    def runall(self, concurrent_samples, sample_runner, all_samples):
        for sample in tqdm(all_samples, desc="Submitting samples"):
            sample_runner(sample)
