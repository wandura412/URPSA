from atoms.atoms import Atom
from molecule.molecule import Molecule


def get_molecules(atomlist, factor=1.1):
    """ separate system into individual molecules"""
    list_of_molecules = []

    while len(atomlist) > 0:
        molecule = Molecule([atomlist[0]])
        atomlist.pop(0)

        no_more_atoms_to_add = False

        while len(atomlist) > 0 and not no_more_atoms_to_add:
            no_more_atoms_to_add = True
            to_remove = []

            for atom_in_molecule in molecule.atoms:
                for alone_atom in atomlist:
                    # Assuming if atoms are in the same molecule then atoms are closer than the sum of c_radius
                    # between their distance
                    if atom_in_molecule.distance_between(alone_atom) < factor * (
                            atom_in_molecule.c_radius + alone_atom.c_radius):
                        to_remove.append(alone_atom)
                        no_more_atoms_to_add = False

            # Add the atoms to the molecule and remove them from atomlist
            for atom in to_remove:
                molecule.add_atom(atom)
                if atom in atomlist:
                    atomlist.remove(atom)  # Ensure atom is in atomlist before attempting to remove

        list_of_molecules.append(molecule)

    return list_of_molecules


def get_atom_list(symbols, opt_coords):
    atomList = []
    xyz = opt_coords
    n=1
    for symbol, coord in zip(symbols, xyz):
        atomList.append(Atom(symbol, *coord,n))
        n += 1

    return atomList


def get_new_molecules(atom_symbols, file):
    a_list = get_atom_list(atom_symbols, file.opt_coords)
    return get_molecules(a_list)


class products_writer:
    def __init__(self, input_file_directory, file="products.txt"):
        self.file = input_file_directory + "/" + file

    def get_the_molecular_string(self, molecules):
        string = ''
        for molecule in molecules:
            string += f"{molecule.number_of_atoms()}\nRMSD {molecule.calculate_RMSD()}" + "\n" + molecule.to_str() + "\n"

        return string

    def save_products(self, molecules: [Molecule]):
        """
        save number of atoms, RMSD, xyz coordinates for each molecule observed.
        :return None:
        """
        string = self.get_the_molecular_string(molecules)
        self.write_products_file(string)

    def get_products_list(self, symbols, output_file_list):
        if len(output_file_list) > 0:
            return self.add_products(symbols, output_file_list)
        else:
            print("no output file is produced")

    def add_products(self, atom_symbols, outputfile_list):
        index = self.find_the_formation_of_products(outputfile_list)
        atom_list = get_atom_list(atom_symbols, outputfile_list[index].opt_coords)
        molecules = get_molecules(atom_list)
        for molecule in molecules:
            print(f"setp-{index} RMSD- {molecule.calculate_RMSD()}")

        self.save_products(molecules)
        return molecules

    def find_the_formation_of_products(self, file_list):
        """ find the minimum energy point"""
        minimum_index = -1
        # for j, i in enumerate(file_list):
        #     if i.is_converged == 0 and i.scf_done <= file_list[minimum_index].scf_done:
        #         minimum_index = j
        #     j += 1
        return minimum_index

    def create_if_not(self):
        try:
            with open(self.file, "a") as _:
                pass
        except:
            with open(self.file, "w") as _:
                pass

    def write_products_file(self, products):
        self.create_if_not()
        with open(self.file, "a") as f:
            f.write(products + "\n")

