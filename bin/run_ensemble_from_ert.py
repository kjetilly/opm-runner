import opm_runner
import argparse
import os
import sys
import subprocess


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        Runs OPM Flow across a set of parameters from an ERT file
    """
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only display the command to run. (will still create augmented files).",
    )
    parser.add_argument(
        "--args-to-flow",
        default=None,
        type=str,
        help="File containing additional arguments to pass to flow. One argument per line.",
    )

    parser.add_argument(
        "--outputdir", required=True, help="Output path (should be a directory)."
    )

    parser.add_argument(
        "--ert-file",
        default=None,
        required=True,
        type=str,
        help="ERT file describing the setup.",
    )

    parser.add_argument(
        "--cpus-per-sample",
        default=1,
        type=int,
        help="Number of CPUs to allocate per sample(where applicable)"
    )

    parser.add_argument("--flowpath", default="flow", help="Path to run flow.")

    args = parser.parse_args()

    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir, exist_ok=True)
    assert os.path.isfile(args.ert_file)
    assert os.path.exists(args.flowpath)
    assert os.path.isfile(args.flowpath)

    ert = opm_runner.fake_ert.parse_ert(args.ert_file)

    arguments = ert.prepare_run_case(args.outputdir)

    if args.dry_run:
        arguments.append("--dry-run")

    if args.args_to_flow is not None:
        arguments.extend(["--args-to-flow", args.args_to_flow])

    arguments.extend(['--cpus-per-sample', str(args.cpus_per_sample)])

    arguments.extend(['--flowpath', args.flowpath])
    runscript = os.path.realpath(sys.argv[0]).replace(
        os.path.basename(sys.argv[0]), "run_ensemble.py"

    )
    command = [sys.executable, runscript, *arguments]

    subprocess.run(command, check=True)
