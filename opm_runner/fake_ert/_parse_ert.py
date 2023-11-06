import collections
from .ert_builder import ERTBuilder
import os

def parse_ert(ertfilepath):
    state = ERTBuilder()

    handler = collections.defaultdict(
        lambda state, keyword, value: print(f"Warning: Ignoring keyword {keyword}.")
    )

    handler.extend(
        {
            "NUM_REALIZATIONS": lambda s, k, v: s.set_number_of_samples(int(v[0])),
            "QUEUE_SYSTEM": lambda s, k, v: s.set_submitter(v[0].lower()),
            "QUEUE_OPTION": lambda s, k, v: s.set_concurrent_samples(int(v[2].lower()))
            if v[0] == "LOCAL" and v[1] == "MAX_RUNNING"
            else None,
            "RUNPATH": lambda s, k, v: s.set_runpath(v[0].split("/")[0]),
            "DATA_FILE": lambda s, k, v: s.set_data_file(v[0]),
            "GEN_KW": lambda s, k, v: s.set_gen_kw(v[1], v[2], v[3]) if v[0] == "MULT_PORO" else print(f"Ignoring GEN_KW {v[0]}."),
            "RANDOM_SEED": lambda s, k, v: s.set_random_seed(int(v[0])),
        }
    )
    with open(ertfilepath) as ertfile:
        for line in ertfile:
            line = line.strip()
            sline = line.split()

            keyword = sline[0]

            handler[keyword](state, keyword, sline[1:])

    state.set_basedir(os.path.dirname(ertfilepath))
    return state.make_ert()
