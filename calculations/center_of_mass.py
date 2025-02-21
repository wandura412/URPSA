def center_of_mass(atoms):
    sum_of_gravity_vector_x_dir = 0
    sum_of_gravity_vector_y_dir = 0
    sum_of_gravity_vector_z_dir = 0
    sum_of_mass = 0

    for atom in atoms:
        sum_of_gravity_vector_x_dir += atom.mass * atom.x
        sum_of_gravity_vector_y_dir += atom.mass * atom.y
        sum_of_gravity_vector_z_dir += atom.mass * atom.z
        sum_of_mass += atom.mass

    return [sum_of_gravity_vector_x_dir / sum_of_mass,
            sum_of_gravity_vector_y_dir / sum_of_mass,
            sum_of_gravity_vector_z_dir / sum_of_mass
            ]
