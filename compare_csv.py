import csv
import os

def main():
    # Get a list of files in the CWD
    compare_path = r".\Compare"
    available_files = os.listdir(compare_path)
    
    # Create a list to store the name of the csv files that we want to compare
    files_to_compare = [file for file in available_files if file.endswith(".csv")]
    print(files_to_compare)

    with open(f"{compare_path}{files_to_compare[0]}", 'r', encoding="utf8") as check_file:
        # check_set = set([row.split(',')[0].strip().upper() for row in check_file])
        check_set = set([row for row in check_file])
        
    with open(f"{compare_path}{files_to_compare[1]}", 'r', encoding="utf8") as in_file, open('difference.csv', 'w') as out_file:
        for line in in_file:
            # if line.split(',')[0].strip().upper() not in check_set:
            if line not in check_set:
                out_file.write(line) 


if __name__ == "__main__":
    main()