from typing import Any, AnyStr
import os


class SampleDir:
    def __init__(self, outputdir, fmtstring="sample_{sample}"):
        self._outputdir = outputdir
        self._fmtstring = fmtstring

    def __call__(self, sample: int) -> AnyStr:
        return os.path.join(self._outputdir, self._fmtstring.format(sample=sample))
