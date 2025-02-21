from inputFileGeneration.input_template import get_input_template
from inputFileGeneration.write_input_file import generate_input_file



def setup_input_file(coordinate, template, system):
    return template + coordinate + system.molecules[0].to_str() + "\n\n\n\n"


def file_name_generator(number,input_file_name="step"):
    return input_file_name + str(number) + ".com"


def input_file_config(number, coordinate_string, system):
    """new file generator """
    template = get_input_template(number, system)
    file_name = file_name_generator(number)
    string_to_be_written = setup_input_file(coordinate_string, template, system)
    generate_input_file(file_name, string_to_be_written)

