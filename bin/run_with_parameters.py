import opm_runner
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        Runs OPM flow with the given parameters.
    """
    )
    parser.add_argument("--inputfile", type=str, help="Input datafile (.DATA)")
    parser.add_argument(
        "--outputdir", required=True, help="Output path (should be a directory)."
    )
    parser.add_argument("--parametersfile", required=True, help="CSV parameter file.")
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
    parser.add_argument("--flowpath", default="flow", help="Path to run flow.")

    args = parser.parse_args()

    assert os.path.isdir(args.outputdir)
    assert os.path.exists(args.parametersfile)
    assert not os.path.isdir(args.parametersfile)
    assert os.path.exists(args.inputfile)
    assert not os.path.isdir(args.inputfile)
    assert os.path.exists(args.flowpath)
    assert os.path.isfile(args.flowpath)

    if os.path.realpath(os.path.dirname(args.inputfile)) == os.path.realpath(
        args.outputdir
    ):
        raise Exception(f"{args.inputfile} is in output directory {args.outputdir}.")

    all_files = opm_runner.find_included_files(args.inputfile)

    parameters = opm_runner.get_parameters_from_file(args.parametersfile)

    if args.dry_run:
        flow = opm_runner.OPMFlow(
            args.flowpath, runner=opm_runner.DryRun(), argsfile=args.args_to_flow
        )
    else:
        flow = opm_runner.OPMFlow(
            args.flowpath, runner=opm_runner.Run(), argsfile=args.args_to_flow
        )

    for filename in all_files:
        outputfilename = os.path.join(args.outputdir, os.path.basename(filename))
        opm_runner.set_parameter_in_file(filename, outputfilename, parameters)

    inputfiletorun = os.path.join(args.outputdir, os.path.basename(args.inputfile))
    flow(inputfiletorun)
