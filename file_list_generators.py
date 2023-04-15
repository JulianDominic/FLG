#! python3
# file_list_generators.py - This program will walk through the directory and generate a CSV that keeps track of the child files

import csv
import os
from datetime import date
from pathlib import Path

def main():
    # Folder to search
    while True:
        directory = input("Enter the file directory: (X:) or (Z:)\n> ")
        if directory == "Z:" or directory == "X:":
            break
        else:
            print("Type exactly 'X:' or 'Z:'")
    file_letter = directory[0]

    # My Folders are already in (Folder A, Folder B, Folder C)
    top_level_folders = set(os.listdir(directory))
    folders_wanted = {"Anime", "Movies", "TV Shows"}
    top_level_folders = sorted(top_level_folders.intersection(folders_wanted))
    for top_level_folder_name in top_level_folders:
        # Get the specific folder to search
        directory = os.path.join(directory, f"\{top_level_folder_name}")
        catalogue = []
        for parent, subdir, file in os.walk(directory):
            parent = clean_path(parent, directory)
            items = (parent, subdir, file)
            # If subdir list is empty, it means that there are only files in the "parent" directory
            if not(subdir):
                catalogue.append({"Folder Path": parent, "File Names": file})
        write_to_csv(file_letter, catalogue, top_level_folder_name)
        print(f"Finished generating the CSV file for {top_level_folder_name}.")
    else:
        print("All the CSV file(s) have been generated!")


def write_to_csv(file_letter, catalogue, top_level_folder_name):
    today = date.today()
    Path(f".\{today}").mkdir(parents=True, exist_ok=True)
    # CSV Headers
    headers = ["Folder Path", "File Name"]
    FILE_EXT = ("mp4", "mkv", "srt")
    non_video_files = []

    # Writing to CSV
    with open(f".\{today}\{top_level_folder_name} Files ({file_letter}).csv", "w", encoding="UTF-8", newline="") as f, open(f".\{today}\{top_level_folder_name} Non-Video Files ({file_letter}).txt", "w", encoding="UTF-8", newline="") as n:
        writer = csv.DictWriter(f, fieldnames=headers)

        # Write the headers
        writer.writeheader()

        # Write each of the individual rows
        for files in catalogue:
            folder_path = files["Folder Path"]
            file_names = files["File Names"]
            for file_name in file_names:
                # If file_name has the a certain file extension, write it to the CSV
                if file_name.endswith(FILE_EXT):
                    writer.writerow({"Folder Path": folder_path, "File Name": file_name})
                else:
                    n.write(f"{folder_path}\{file_name}\n")


def clean_path(path, directory):
    return path.replace(directory, "")


if __name__ == "__main__":
    main()
