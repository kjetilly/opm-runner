import os
import sys


class SampleRunner:
    def __init__(
        self,
        *,
        submitter,
        script,
        inputfile,
        flowpath,
        args_to_flow,
        dry_run,
        sampledir,
    ):
        self._submitter = submitter
        self._script = script
        self._inputfile = inputfile
        self._flowpath = flowpath
        self._args_to_flow = args_to_flow
        self._dry_run = dry_run
        self._sampledir = sampledir

    def __call__(self, sampleid):
        arguments_to_sample = [
            sys.executable,
            self._script,
            "--inputfile",
            self._inputfile,
            "--outputdir",
            self._sampledir(sampleid),
            "--parametersfile",
            os.path.join(self._sampledir(sampleid), "parameters.txt"),
            "--flowpath",
            self._flowpath,
        ]
        if self._dry_run:
            arguments_to_sample.append("--dry-run")
        if self._args_to_flow is not None:
            arguments_to_sample.append(f"--args_to_flow={self._args_to_flow}")
        stdoutfile = os.path.join(self._sampledir(sampleid), "flow.stdout")
        stderrfile = os.path.join(self._sampledir(sampleid), "flow.stderr")

        self._submitter(
            arguments_to_sample,
            check=True,
            stderrfile=stderrfile,
            stdoutfile=stdoutfile,
        )

        return sampleid
