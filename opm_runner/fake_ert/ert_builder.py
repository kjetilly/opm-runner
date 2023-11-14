from .ert import ERT


class ERTBuilder:
    def __init__(self) -> None:
        self.submitter = None
        self.number_of_samples = None
        self.concurrent_samples = 1
        self.runpath = None
        self.data_file = None
        self.gen_kw = None
        self.random_seed = None
        self.basedir = None
        self.sample_dir_fmt = None

    def set_submitter(self, submitter):
        self.submitter = submitter

    def set_number_of_samples(self, samples):
        self.number_of_samples = samples

    def set_concurrent_samples(self, concurrent_samples):
        self.concurrent_samples = concurrent_samples

    def set_runpath(self, runpath, sample_dir_fmt):
        self.runpath = runpath
        self.sample_dir_fmt = sample_dir_fmt.replace('%d', '{sample}', 1).replace('%d', '0')

    def set_data_file(self, data_file):
        self.data_file = data_file

    def set_gen_kw(self, templatefile, outputfile, parameterfile):
        self.gen_kw = {
            "templatefile": templatefile,
            "outputfile": outputfile,
            "parameterfile": parameterfile,
        }

    def set_random_seed(self, random_seed):
        self.random_seed = random_seed

    def set_basedir(self, basedir):
        self.basedir = basedir

    def make_ert(self):
        assert self.submitter is not None
        assert self.number_of_samples is not None
        assert self.concurrent_samples is not None and self.concurrent_samples >= 1
        assert self.runpath is not None
        assert self.data_file is not None
        assert self.gen_kw is not None
        assert self.random_seed is not None
        assert self.basedir is not None
        assert self.sample_dir_fmt is not None

        return ERT(
            submitter=self.submitter,
            number_of_samples=self.number_of_samples,
            concurrent_samples=self.concurrent_samples,
            runpath=self.runpath,
            data_file=self.data_file,
            gen_kw=self.gen_kw,
            random_seed=self.random_seed,
            basedir = self.basedir,
            sample_dir_fmt = self.sample_dir_fmt
        )
