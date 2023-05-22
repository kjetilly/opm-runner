import re
import os.path

def find_included_files(deckfile):
    included_files = [deckfile]
    basepath = os.path.dirname(deckfile)
    with open(deckfile) as f:
        include_found = False
        for line in f:
            if line.strip().lower().startswith("include"):
                include_found = True
                current_filename = ""
                line = re.sub("(?i)include","", line)
            if include_found:
                current_filename += line.replace("/", ""). strip().replace("'", "")
                if line.strip().endswith('/'):
                    include_found = False
                    current_filename = current_filename.strip()
                    current_filename = os.path.join(basepath, current_filename)
                    included_files.extend(find_included_files(current_filename))
    return included_files
            


            