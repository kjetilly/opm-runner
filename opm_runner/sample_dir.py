from typing import Any, AnyStr
import os


class SampleDir:
    def __init__(self, outputdir):
        self._outputdir = outputdir

    def __call__(self, sample: int) -> AnyStr:
        return os.path.join(self._outputdir, f"sample_{sample}")
