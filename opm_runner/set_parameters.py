from typing import Dict

def make_template_parameter(parameter_name: str):
    return f"<{parameter_name}>"

def set_parameter_in_file(filename_input, filename_output, parameters: Dict[str, str]):
    with open (filename_input, 'r') as finput:
        with open(filename_output, 'w') as foutput:
            for line in finput:
                for parameter_name, parameter_value in parameters.items():
                    templated_parameter_name = make_template_parameter(parameter_name)
                    line = line.replace(templated_parameter_name, parameter_value)
                foutput.write(line)

def set_parameters_in_files(filenames_in_out: Dict[str, str], parameters: Dict[str, str]):
    for filename_in, filename_out in filenames_in_out.items():
        set_parameter_in_file(filename_in, filename_out, parameters)
