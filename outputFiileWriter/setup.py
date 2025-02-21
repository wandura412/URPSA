import os
import re
import sys


class Setup:

    def __init__(self,name):
        # self.project_dir = "Projects/"+name
        self.project_dir = name
        self.project_exists()

    def project_exists(self):
        if not os.path.exists(self.project_dir):
            os.makedirs(self.project_dir)
        else:
            print(f"project name '{self.project_dir}' already exists.")
            sys.exit()

    def check_dir_in_the_project(self):
        """Get all folders in the directory and inside the 'archives' folder, then sort them by their number 'test_00001'."""
        all_dirs = []

        # Get folders in the main directory
        main_dirs = [d for d in os.listdir(self.project_dir) if os.path.isdir(os.path.join(self.project_dir, d))]
        all_dirs.extend(main_dirs)

        # Check if 'Archive' folder exists and get its subfolders
        archives_path = os.path.join(self.project_dir, 'Archives')
        if os.path.exists(archives_path) and os.path.isdir(archives_path):
            archive_dirs = [d for d in os.listdir(archives_path) if os.path.isdir(os.path.join(archives_path, d))]
            all_dirs.extend([os.path.join('Archives', d) for d in archive_dirs])

        def extract_number(folder_name):
            match = re.search(r'\d+', folder_name)
            return int(match.group()) if match else -1

        sorted_dirs = sorted(all_dirs, key=extract_number)
        return sorted_dirs


    def get_next_folder_number(self):
        """Generate the next folder name in the sequence"""
        sorted_dirs = self.check_dir_in_the_project()
        return len(sorted_dirs)+1

    def get_next_folder_name(self):
        """Generate the next folder name in the sequence"""
        sorted_dirs = self.check_dir_in_the_project()
        if not sorted_dirs:
            next_number = 1
        else:
            def extract_number(folder_name):
                match = re.search(r'\d+', folder_name)
                return int(match.group()) if match else -1

            highest_number = extract_number(sorted_dirs[-1])
            next_number = highest_number + 1

        next_folder_name = f"Pathway_{next_number:05d}"
        print(f"Next folder name: {next_folder_name}")

        return next_folder_name