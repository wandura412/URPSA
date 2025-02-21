import json

class productsManager:
    def __init__(self, dir, name="products.json"):
        self.file = dir+name
        self.indent=4

    def read(self):
        with open(self.file, "r") as file:
            data = json.load(file)
        return data


    def create_if_not(self):
        try:
            with open(self.file, "a") as _:
                pass
        except:
            with open(self.file, "w") as _:
                pass

    def write_product(self, iter, molecules,energy=0):

        #todo: pass energy
        if molecules == [] or molecules is None:
            print("No molecules are found")
            return
        self.create_if_not()
        new_data = self.create_json_string(molecules,energy)
        try:
            data = self.read()
            data[int(iter)] = new_data
        except:
            data ={int(iter):new_data}


        with open(self.file,"w") as file:
            file.write(json.dumps(data, indent=self.indent))


    def create_json_string(self, molecules,energy):

        molecule_list =[]
        for molecule in molecules:
            molecule_list.append({f"RMSD":molecule.calculate_RMSD(), "molecule":molecule.to_str()})
        dict = { "num_of_molecules": len(molecules),"energy":energy , "molecules": molecule_list}

        return dict

    def check_number_of_times_same_products_were_observed(self,iter,moleculs):
        if moleculs is None:
            return -1
        number_of_times = 0
        current_rmsds = [molecule.calculate_RMSD() for molecule in moleculs]
        data = self.read()


        for i in range(iter):
            rmsd_list = []
            try:
                for j in data[str(i)]['molecules']:
                    rmsd_list.append(j["RMSD"])
                    if self.almost_equal_RMSD(current_rmsds, rmsd_list):
                        number_of_times += 1
            except:
                    pass


        return number_of_times


    def almost_equal_RMSD(self, list1, list2,possible_change=0.05):
        for i, j in zip(list1,list2):
            if i < j:
                if i+possible_change < j:
                    return False
            else:
                if i+possible_change > j:
                    return False
        return True

