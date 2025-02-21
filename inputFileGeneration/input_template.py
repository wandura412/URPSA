def get_input_template(number, system,inp_dir):
    # gonna replace title value
    return f"""%NProcShared={system.number_of_cores}
%Mem={system.memory}
%chk={inp_dir}/test{number}.chk
{system.method}

step{number}
 
{system.charge} {system.multiplicity}	\n"""


