class OutputWriter:

    def __init__(self, input_file_directory,file="output2.xyz"):
        self.file = input_file_directory + "/" + file

    def create_if_not(self):
        try:
            with open(self.file, "a") as _:
                pass
        except:
            with open(self.file, "w") as _:
                pass

    def write_xyz_file(self, sys, opt_xyz):
        self.create_if_not()
        with open(self.file, "a") as f:
            f.write(sys.string_optimized_coordinates(opt_xyz))
