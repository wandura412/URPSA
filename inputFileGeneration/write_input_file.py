


import os


def generate_input_file(file_name,input_file_directory, data):
    # just write to the file
    if input_file_directory not in os.listdir():
        try:
            os.mkdir(input_file_directory)
        except FileExistsError:
            pass

    with open(input_file_directory+'/'+file_name, 'w') as input_file:
        input_file.write(data)

