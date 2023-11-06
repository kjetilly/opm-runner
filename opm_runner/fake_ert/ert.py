import os
import numpy as np
import csv
import shutil
import sys


class ERT:
    def __init__(
        self,
        *,
        submitter,
        number_of_samples,
        concurrent_samples,
        runpath,
        data_file,
        gen_kw,
        random_seed,
        basedir
    ):
        self.submitter = submitter
        self.number_of_samples = number_of_samples
        self.concurrent_samples = concurrent_samples
        self.runpath = runpath
        self.data_file = data_file
        self.gen_kw = gen_kw
        self.random_seed = random_seed
        self.basedir = basedir

    def _make_case_file(self, outputdir):
        os.makedirs(outputdir, exist_ok=True)

        # TODO: Factor out this parsing here
        all_parameters = {}
        ert_parameterfilename = os.path.join(self.basedir, self.gen_kw['parameterfile'])
        with open(ert_parameterfilename) as f:
            for l in f:
                ls = l.split()
                parameter_name = l[0]
                assert ls[1] == 'UNIFORM'
                vmin = float(ls[2])
                vmax = float(ls[3])
                all_parameters[parameter_name] = np.random.uniform(vmin, vmax, self.number_of_samples)

        parameterfilename = os.path.join(outputdir, "parameters.csv")
        with open(parameterfilename, "w") as parameterfile:
            writer = csv.DictWriter(parameterfile, fieldnames=list(all_parameters.keys()))
            writer.writeheader()

            for n in range(self.number_of_samples):
                writer.writerow({k: v[n] for k, v in all_parameters.items()})
        
        casedir = os.path.basename(os.path.dirname(self.data_file))
        outputcasedir = os.path.join(outputdir, casedir)
        os.makedirs(outputcasedir, exist_ok=True)

        data_file = os.path.join(outputcasedir, os.path.basename(self.data_file))
        shutil.copy(self.data_file, data_file)

        template_file = os.path.join(outputcasedir, os.path.basename(self.gen_kw['outputfile']))
        template_file_source = os.path.join(self.basedir, os.path.basename(self.gen_kw['templatefile']))
        shutil.copyfile(template_file_source, template_file)

        return parameterfilename, data_file
    
    def prepare_run_case(self, outputdir):
        parameterfilename, data_file = self._make_case_file(outputdir)
        
        return [
            '--inputfile', data_file,
            '--outputdir', os.path.join(outputdir, self.runpath),
            '--parametersfile', parameterfilename,
            '--concurrent-samples', self.concurrent_samples,
            '--submitter', self.submitter
        ]


