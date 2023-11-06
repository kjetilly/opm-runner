from .submitter import Submitter
import subprocess
import tqdm
import multiprocessing


class Bash(Submitter):
    def __call__(self, cli, stderrfile=None, stdoutfile=None, check=True):
        with open(stderrfile, "w") as err:
            with open(stdoutfile, "w") as out:
                return subprocess.run(cli, check=check, stdout=out, stderr=err)

    def waitall(self):
        return True

    def runall(self, concurrent_samples, sample_runner, all_samples):
        with multiprocessing.Pool(concurrent_samples) as pool:
            # Get a nice TQDM bar, see for instance:https://stackoverflow.com/questions/41920124/multiprocessing-use-tqdm-to-display-a-progress-bar
            for _ in tqdm.tqdm(
                pool.imap(sample_runner, all_samples), total=len(all_samples), desc='Running'
            ):
                pass