
""" go to log files directory starts reading them and log files from log files folder then
 grab the data required.
 """

import os, re


def input_file_validator(file_name):
    return file_name[-3:] == 'com'


def get_input_files_list(input_file_directory):
    input_files_list = os.listdir(input_file_directory)
    input_files_list = [file for file in input_files_list if input_file_validator(file)]
    return order_input_files(input_files_list)


def order_input_files(input_files):
    def extract_number(file):
        # Use regular expression to extract the number from the name
        match = re.search(r'\d+', file)
        return int(match.group()) if match else 0

    # Sort the names based on the extracted numbers
    sorted_names = sorted(input_files, key=extract_number)

    return sorted_names


def find_corresponding_output_file(inputfile):
    return inputfile[:-3]+"log"





