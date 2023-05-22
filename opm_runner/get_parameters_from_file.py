import csv
def get_parameters_from_file(filename):
    with open(filename) as f:
        csvfile = csv.DictReader(f)
        for line in csvfile:
            # TODO: Do we need this conversion here?
            return {k: v for k,v in line.items()}