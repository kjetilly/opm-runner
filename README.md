# opm-runner

A small, really simple tool to run OPM Flow with various parameters. This is utility is **very** bare bones, and is not supposed to do a lot. 

# Setting up

You should probably make a new virtualenv and install the requirements:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Running

Suppose you have the datafile `INPUTDATA.DATA` and want to store the output in `OUTPUTDIR` (which should be created by you beforehand), then one could run:

```
python bin/run_ensemble.py \
    --outputdir=OUTPUTDIR \
    --inputfile INPUTDATA.DATA \
    --parametersfile=test_data/input_params.csv  \
    --flowpath=/path/to/flow
    --concurrent-samples=1
```

# Running upscaled SPE1

To run the upscaled SPE1 example included, run

```bash
python bin/run_ensemble.py \
    --inputfile test_data/spe1/SPE1ENSEMBLE.DATA \
    --outputdir testdir \
    --parametersfile test_data/montecarlo.csv \
    --flowpath /path/to/flow \
    --concurrent-samples=1
```

