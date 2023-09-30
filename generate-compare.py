#! python3
# generate-compare.py - Generate CSVs for directories in different drives, compare them, and generate new CSVs with the differences.

import csv
import os
from datetime import date
from pathlib import Path

DRIVE_LETTER_1 = 'X'
DRIVE_LETTER_2 = 'Z'
DRIVES_TO_SEARCH = [DRIVE_LETTER_1, DRIVE_LETTER_2]
FOLDERS_WANTED = ["Anime", "Movies", "TV Shows"]
FILE_EXTS_WANTED = ("mp4", "mkv", "srt")
TODAY = date.today()  # YYYY-MM-DD


def main():
    generate_csv()
    compare_csv()


def generate_csv() -> None:
    for drive in DRIVES_TO_SEARCH:
        # 'X' + ':' = "X:""
        drive = drive + ":"
        for folder_name in FOLDERS_WANTED:
            # Create a folder_path -- X:\Anime, Z:\Anime, etc
            folder_path = os.path.join(drive, folder_name)
            catalogue = []
            print("Searching for files...")
            for parent_directory, sub_directory, file in os.walk(folder_path):
                # Get rid of the folder_path that is written in the parent_directory
                parent_directory = parent_directory.lstrip(drive).lstrip(folder_name).lstrip('\\')
                # If the sub_directory list is empty, it means that we have reached the bottom/end of the folder and we can now find files
                if not(sub_directory):
                    catalogue.append({"Path": parent_directory, 
                                      "File": file})
            print("Finished searching.")
            write_to_csv(drive[0], catalogue, folder_name)
    else:
        print("All CSVs have been generated.\n\n")


def compare_csv() -> None:
    Path(f".\{TODAY}\Differences").mkdir(parents=True, exist_ok=True)
    available_files = os.listdir(f".\{TODAY}\Raw\\")
    # Create a dictionary that contains the folder_name as the key and a list of .csv files to compare as the value
    compare_dict = {}
    for folder_name in FOLDERS_WANTED:
        compare_dict[folder_name] = []
        for file in available_files:
            if file.endswith(".csv"):
                check_folder_name = file.split('-')
                if folder_name in check_folder_name:
                    compare_dict[folder_name].append(file)
        print(f"Starting the comparison for {folder_name}...")
        # It just so happens that in compare_dict, our files are already in DRIVE_LETTER_1 and DRIVE_LETTER_2 order.
        # Since I know that DRIVE_LETTER_1 is the drive that contains less info, it will be used as the "master".
        with open(f".\{TODAY}\Raw\{compare_dict[folder_name][0]}", 'r', encoding="utf8") as check_file:
            check_set = set([row for row in check_file])
        with open(f".\{TODAY}\Raw\{compare_dict[folder_name][1]}", 'r', encoding="utf8") as in_file, \
            open(f'.\{TODAY}\Differences\{folder_name} Differences.csv', 'w') as out_file:
            for line in in_file:
                # If the file is not found in DRIVE_LETTER_1, we will write a line to the CSV.
                if line not in check_set:
                    out_file.write(line)
        print(f"Finished the comparison for {folder_name}.\n")
    else:
        print("All tasks have been completed.")


def write_to_csv(drive:str, catalogue:list, folder_name:str) -> None:
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
