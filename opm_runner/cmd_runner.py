import subprocess

class DryRun:
    def __call__(self, cmd, *args, **kwargs):
        print(f"Would run:\n\t{' '.join(cmd)}\n with [{', '.join(args)}] and {kwargs}")

class Run:
    def __call__(self, *args, **kwargs):
        return subprocess.run(*args, **kwargs)