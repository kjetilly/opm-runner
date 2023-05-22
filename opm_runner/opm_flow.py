from .cmd_runner import Run
import os.path


class OPMFlow:
    def __init__(self, flowpath, runner=Run(), argsfile=None):
        self.flowpath = flowpath
        self.runner = runner
        self.args = []
        if argsfile is not None:
            with open(argsfile) as f:
                for l in f:
                    self.args.append(l.strip())

    def __call__(self, inputfile):
        self.runner([
            self.flowpath,
            f'--output-dir={os.path.dirname(inputfile)}',
            *self.args,
            inputfile
        ], check=True)