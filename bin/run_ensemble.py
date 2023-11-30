import opm_runner
import argparse
import os
import csv
import sys
import multiprocessing
import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        Runs OPM Flow across a set of parameters
    """
    )
    parser.add_argument(
        "--inputfile", required=True, type=str, help="Input datafile (.DATA)"
    )
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
    parser.add_argument(
        "--concurrent-samples",
        type=int,
        default=1,
        help="Number of concurrent samples to run.",
    )
    parser.add_argument(
        "--submitter",
        type=str,
        default="bash",
        help="Submitter to use. Options: bash, hq.",
    )
    parser.add_argument(
        "--sample-dir-fmt",
        type=str,
        default="sample_{sample}",
        help="Sample dir format string. Use {sample} to reference the sample number."
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

    sampledir = opm_runner.SampleDir(args.outputdir, fmtstring=args.sample_dir_fmt)

    all_samples = []
    with open(args.parametersfile) as f:
        reader = csv.DictReader(f)
        for l in reader:
            sampleid = l[""]
            all_samples.append(sampleid)
            sdir = sampledir(sampleid)
            os.makedirs(sdir, exist_ok=True)

            with open(os.path.join(sdir, "parameters.txt"), "w") as parout:
                # TODO: Write with the csv package instead.
                keys = list(l.keys())

                values = [l[k] for k in keys]
                parout.write(",".join(keys))
                parout.write("\n")
                parout.write(",".join(values))
                parout.write("\n")

    submitter = opm_runner.submitter.make_submitter(args.submitter, args.cpus_per_sample)
    runscript = os.path.realpath(sys.argv[0]).replace(
        os.path.basename(sys.argv[0]), "run_with_parameters.py"
    )

    sample_runner = opm_runner.SampleRunner(
        submitter=submitter,
        script=runscript,
        inputfile=args.inputfile,
        flowpath=args.flowpath,
        args_to_flow=args.args_to_flow,
        dry_run=args.dry_run,
        sampledir=sampledir,
    )

    submitter.runall(args.concurrent_samples, sample_runner, all_samples)
    submitter.waitall()