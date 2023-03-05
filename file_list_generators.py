#! python3
# file_list_generators.py - Generate CSV and txt files to track what files are available.

import csv
import os
from datetime import date
from pathlib import Path

def main():
    # Folder to search
    dir="Z:"
    file_letter = dir[0]

    # My Folders are already in (Folder A, Folder B, Folder C)
    top_level_folders = os.listdir(dir)
    for top_level_folder_name in top_level_folders:
        # Get the specific folder to search
        dir = os.path.join(dir, f"\{top_level_folder_name}")
        catalogue = []
        for parent, subdir, file in os.walk(dir):
            parent = clean_path(parent, dir)
            items = (parent, subdir, file)
            # If subdir list is empty, it means that there are only files in the "parent" directory
            if not(subdir):
                catalogue.append({"Folder Path": parent, "File Names": file})
        write_to_csv(file_letter, catalogue, top_level_folder_name)
        print(f"Finished generating the file(s) for {top_level_folder_name}.")


def write_to_csv(file_letter, catalogue, top_level_folder_name):
    today = date.today()
    Path(f".\{file_letter}\{top_level_folder_name}\{today}").mkdir(parents=True, exist_ok=True)

    # CSV Headers
    headers = ["Folder Path", "File Name"]
    
    # Writing to CSV
    video_ext = ("mp4", "mkv", "srt")
    non_video_files = []
    
    with open(f".\{file_letter}\{top_level_folder_name}\{today}\{top_level_folder_name}_Files-{file_letter}.csv", "w", encoding="UTF-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)

        # Write the headers
        writer.writeheader()

        # Write each of the individual rows
        for i in catalogue:
            folder_path = i["Folder Path"]
            file_names = i["File Names"]
            for file_name in file_names:
                file_name: str
                if file_name.endswith(video_ext):
                    writer.writerow({"Folder Path": folder_path, "File Name": file_name})
                else:
                    non_video_files.append(file_name)

    # Create .txt file to track the non video files (exlcuding srt)
    with open(f".\{file_letter}\{top_level_folder_name}\{today}\{top_level_folder_name}_Non-Video_Files-{file_letter}.txt", "w", encoding="UTF-8", newline="") as n:
        for item in non_video_files:
            n.write(item + "\n")



def clean_path(path, dir):
    return path.replace(dir, "")



if __name__ == "__main__":
    main()