#! python3
# generate-compare.py - Generate CSVs for directories in different drives, compare them, and generate new CSVs with the differences.

import csv
import os
from datetime import date
from pathlib import Path

# Config
# TODO: Use Paths instead of Drive Letters
PATH_1 = 'X:\\'  # Use absolute path
PATH_2 = 'Z:\\'  # Z:\
PATHS_TO_SEARCH = [PATH_1, PATH_2]
FOLDERS_WANTED = ["Anime", "Movies", "TV Shows"]
FILE_EXTS_WANTED = ("mp4", "mkv", "srt", ".py")
TODAY = date.today()  # YYYY-MM-DD


def main():
    generate_csv()
    compare_csv()


def generate_csv() -> None:
    """
    Uses the name of the parent folders (Anime, Movies, TV Shows) as the folders to compare later on.
    This function creates CSV files based on the files that are present in these parent folders.
    """
    for path in PATHS_TO_SEARCH:
        drive_letter = path[0]
        for folder_name in FOLDERS_WANTED:
            # Create a folder_path -- X:\Anime, Z:\Anime, etc
            folder_path = os.path.join(path, folder_name)
            catalogue = []
            print("Searching for files...")
            for parent_directory, sub_directory, file in os.walk(folder_path):
                # Get rid of the folder_path that is written in the parent_directory
                parent_directory = parent_directory.lstrip(path).lstrip(folder_name).lstrip('\\')
                # If the sub_directory list is empty, 
                # it means that we have reached the bottom/end of the folder 
                # and we can now find files
                if not(sub_directory):
                    catalogue.append({"Path": parent_directory, 
                                      "File": file})
            print("Finished searching.")
            write_to_csv(drive_letter, catalogue, folder_name)
    else:
        print("All CSVs have been generated.\n\n")


def compare_csv() -> None:
    """
    Group the files that are going to be compared later based on the parent folders (Anime, Movies, TV Shows).
    This function creates CSV files that uses the file with the "missing files" as the checklist,
    and writes a CSV that contains what's missing.
    """
    Path(f".\{TODAY}\Differences").mkdir(parents=True, exist_ok=True)
    available_files = os.listdir(f".\{TODAY}\Raw\\")
    # Create a dictionary that contains the folder_name as the key 
    # and a list of .csv files to compare as the value
    compare_dict = {}
    for folder_name in FOLDERS_WANTED:
        compare_dict[folder_name] = []
        for file in available_files:
            if file.endswith(".csv"):
                check_folder_name = file.split('-')
                if folder_name in check_folder_name:
                    compare_dict[folder_name].append(file)
        # Eliminate the need of choosing which is the "master" by checking both files for differences instead.
        print(f"Starting the comparison for {folder_name}...")
        for i, j in zip([0, 1], [1, 0]):
            csv_1, csv_2 = compare_dict[folder_name][i], compare_dict[folder_name][j]
            csv_1_filename = csv_1.rstrip(".csv")
            with open(f".\{TODAY}\Raw\{csv_1}", 'r', encoding="UTF-8") as base_csv, \
                open(f".\{TODAY}.\Raw\{csv_2}", 'r', encoding="UTF-8") as adjusted_csv:
                base = set(base_csv.readlines())
                adjusted = set(adjusted_csv.readlines())
            # Write the missing entries for base_csv
            with open(f".\{TODAY}\Differences\{csv_1_filename}-Differences.csv", 'w', encoding="utf8") as differences_csv:
                differences = sorted(adjusted.difference(base))
                for line in differences:
                    differences_csv.write(line)
        print(f"Finished the comparison for {folder_name}.\n")
    else:
        print("All tasks have been completed.")


def write_to_csv(drive:str, catalogue:list, folder_name:str) -> None:
    """
    This function creates a CSV file based on the contents in catalogue (Path, File), and uses drive & folder_name
    just for its own file name.
    """
    Path(f".\{TODAY}\Raw").mkdir(parents=True, exist_ok=True)
    csv_headers = ["Path", "File"]
    # Write to CSV
    print("Generating CSV...")
    with open(f".\{TODAY}\Raw\{drive}-{folder_name}-files.csv", 'w', encoding="UTF-8", newline="") as f, \
        open(f".\{TODAY}\Raw\{drive}-{folder_name}-NON-VIDEO-files.txt", 'w', encoding="UTF-8", newline="") as n:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        # Write the headers
        writer.writeheader()
        # Write the rest of the csv
        for item in catalogue:
            path, files = item["Path"], item["File"]
            for file in files:
                if file.endswith(FILE_EXTS_WANTED):
                    writer.writerow({"Path": path,
                                     "File": file})
                else:
                    n.write(f"{path}\{file}\n")
    print(f"Generated {drive}'s {folder_name} CSV.\n")


if __name__ == "__main__":
    main()
