import os
import shutil


def move_dir_to_archive(pathway_dir):
    arc_dir = os.path.join(pathway_dir, '../Archives/', os.path.basename(pathway_dir))
    # Check if the directory exists, if not, create it
    if not os.path.exists(arc_dir):
        os.makedirs(arc_dir)
        print(f"Created archive directory: {arc_dir}")


    try:
        os.rename(pathway_dir, arc_dir)
        print(f"Moved {pathway_dir} to {arc_dir}")
    except FileNotFoundError:
        print("The source directory does not exist.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"Error: {e}")



def delete_dir(source_dir):
    try:
        shutil.rmtree(source_dir)
        print(f"Removed {source_dir}")

    except FileNotFoundError:
        print("The source directory does not exist.")

    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"Error: {e}")

