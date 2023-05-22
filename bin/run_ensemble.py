import opm_runner
import argparse
import os
import csv
import sys
import subprocess
import multiprocessing
import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        Runs OPM Flow across a set of parameters
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
    parser.add_argument(
        "--concurrent-samples", type=int, default=1, 
        help="Number of concurrent samples to run."
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

    sampledir = lambda sample: os.path.join(args.outputdir, f"sample_{sample}")

    all_samples = []
    with open(args.parametersfile) as f:
        reader = csv.DictReader(f)
        for l in reader:
            sampleid = l['']
            all_samples.append(sampleid)
            sdir = sampledir(sampleid)
            os.makedirs(sdir, exist_ok=True)

            with open(os.path.join(sdir, 'parameters.txt'), 'w') as parout:
                # TODO: Write with the csv package instead.
                keys = list(l.keys())
                
                values = [l[k] for k in keys]
                parout.write(",".join(keys))
                parout.write("\n")
                parout.write(",".join(values))
                parout.write("\n")

    def run_for_sample(sampleid):
        arguments_to_sample = [
            sys.executable, 
            os.path.realpath(sys.argv[0]).replace(os.path.basename(sys.argv[0]), "run_with_parameters.py"),
            "--inputfile", args.inputfile,
            "--outputdir", sampledir(sampleid),
            "--parametersfile", os.path.join(sampledir(sampleid), 'parameters.txt'),
            '--flowpath', args.flowpath
        ]
        if args.dry_run:
            arguments_to_sample.append('--dry-run')
        if args.args_to_flow is not None:
            arguments_to_sample.append(f'--args_to_flow={args.args_to_flow}')
        with open(os.path.join(sampledir(sampleid), "flow.stdout"), "w") as stdoutfile:
            with open(os.path.join(sampledir(sampleid), "flow.stderr"), "w") as stderrfile:
                subprocess.run(arguments_to_sample, check=True, stderr=stderrfile, stdout=stdoutfile)

        return sampleid

    with multiprocessing.Pool(args.concurrent_samples) as pool:  
        # Get a nice TQDM bar, see for instance:https://stackoverflow.com/questions/41920124/multiprocessing-use-tqdm-to-display-a-progress-bar
        for _ in tqdm.tqdm(pool.imap(run_for_sample, all_samples), total=len(all_samples)):
            pass
