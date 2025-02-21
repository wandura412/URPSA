
import numpy as np
from atoms.atoms import Atom
from molecule.molecule import Molecule


def spherically_converge_to_center(molecule, size=0.1):
    """
    Moves a molecule or atom incrementally toward the origin in a spherical trajectory.

    This function calculates the unit vector of the molecule's current position and moves it
    closer to the origin by a step size. The new position is updated in the molecule object.

    :param molecule: The molecule object with methods to get and update its coordinates.
    :param size: Step size for each iteration (float). Default is 0.1.
    :return: A list [x, y, z] representing the new position of the molecule.
    ;modify molecule: Updates the molecule's position to the new coordinates.
    """
    position_vector = np.array(molecule.get_coords())
    unit_vector = np.array(molecule.unit_position_vector())
    new_position = position_vector - size * unit_vector
    molecule.update_coordinates(*new_position)
    return new_position


def move_atoms_towards_center(molecule, size):
    for atom in molecule.atoms:
        spherically_converge_to_center(atom, size)


def push_fragments_to_center(molecules, step_size=1):
    """
    this functions converges atoms to the origin

    :param molecules: (list of molecule objects)
    :param step_size: (int)
    :Modify : modify molecules, atoms
    :return molecules: None
    """

    for molecule in molecules:
        spherically_converge_to_center(molecule, step_size)



if __name__ == "__main__":
    print(spherically_converge_to_center(Molecule([Atom("Si", 1, 1, 1)])))

