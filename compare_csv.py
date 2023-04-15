#! python3
# compare_csv.py - This program is used to find the differences in the entries of two different CSVs.

import csv
import os

def main():
    cwd = os.listdir()
    if "Differences" not in cwd:
        os.mkdir("Differences")
    # Get a list of files in the CWD
    compare_path = r".\Compare\\"
    available_files = os.listdir(compare_path)
    
    # Create a list to store the name of the csv files that we want to compare
    files_to_compare = [file for file in available_files if file.endswith(".csv")]
    for idx, file in enumerate(files_to_compare):
        print(f"[{idx}]. {file}")
    print()
    max_idx = len(files_to_compare) - 1

    choice_flag = True
    while choice_flag:
        while True:
            first_file = input("Enter the number of the first file you want to compare:\n> ")
            if first_file.isdecimal() and 0 <= int(first_file) <= max_idx:
                first_file = int(first_file)
                break
        while True:
            second_file = input("Enter the number of the second file you want to compare:\n> ")
            if (second_file.isdecimal()) and (0 <= int(second_file) <= max_idx):
                if (first_file == second_file):
                    print("You can't compare the same file!")
                    continue
                else:
                    second_file = int(second_file)
                    break
        first = files_to_compare[first_file]
        second = files_to_compare[second_file]
        files_to_compare = [first, second]
        prompt = input(f"Are you sure you want to compare {files_to_compare}? (Y/N)\n> ")
        if prompt.upper() == "Y":
            choice_flag = False
        elif prompt.upper() == "N":
            continue
        else:
            print("Invalid option")
            continue
    
    filename_flag = True
    while filename_flag:
        filename = input("Enter the name of the output file (It will appear as '<FILENAME> Differences.csv'):\n> ")
        prompt = input(f"Are you sure you want to name it '{filename} Differences.csv'? (Y/N)\n> ")
        if prompt.upper() == "Y":
            filename_flag = False
        elif prompt.upper() == "N":
            continue
        else:
            print("Invalid option")
            continue

    print(f"Comparing the files; {files_to_compare}")
    with open(f"{compare_path}{files_to_compare[0]}", 'r', encoding="utf8") as check_file:
        check_set = set([row for row in check_file])
        
    with open(f"{compare_path}{files_to_compare[1]}", 'r', encoding="utf8") as in_file, open(f'.\Differences\{filename} Differences.csv', 'w') as out_file:
        for line in in_file:
            if line not in check_set:
                out_file.write(line) 


if __name__ == "__main__":
    main()
    print("The comparison has been completed.")
