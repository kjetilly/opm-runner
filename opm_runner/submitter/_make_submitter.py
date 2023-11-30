from .bash import Bash
from .dry_run import DryRun
from .hq import HQ


def make_submitter(submitter_name, cpus_per_sample):
    if submitter_name == 'bash':
        return Bash()
    elif submitter_name == 'dry_run':
        return DryRun()
    elif submitter_name == 'hq':
        return HQ(cpus_per_sample)
    else:
        raise ValueError(f"Uknown submitter {submitter_name}.")