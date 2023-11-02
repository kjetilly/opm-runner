from .bash import Bash
from .dry_run import DryRun
from .hq import HQ


def make_submitter(submitter_name):
    if submitter_name == 'bash':
        return Bash()
    elif submitter_name == 'dry_run':
        return DryRun()
    elif submitter_name == 'HQ':
        return HQ()
    else:
        raise ValueError(f"Uknown submitter {submitter_name}.")