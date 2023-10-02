import os
from pathlib import Path

def main():
    available_files = [file for file in os.listdir(".") if file.endswith(".csv")]
    num_available_files = len(available_files)
    if num_available_files < 2:
        input(f"There are not enough files to compare.\nThere is/are only {num_available_files} files available.\n\nPress Enter to exit.")
        return
    elif num_available_files == 2:
        compare_csv(available_files)
    else:
        # TODO: Add option validation
        print("Select the first file to compare:")
        for index, file in enumerate(available_files):
            print(f"\t[{index:2d}]. {file}")
        option_1 = int(input("Option: "))
        csv_1 = available_files[option_1]
        print("\n")
        print("Select the second file to compare:")
        for index, file in enumerate(available_files):
            # Skip the option that was already chosen
            if index == option_1:
                continue
            print(f"\t{index}. {file}")
        option_2 = int(input("Option: "))
        csv_2 = available_files[option_2]

        compare_csv([csv_1, csv_2])

def compare_csv(files_to_compare:list[str]) -> None:
    Path(f".\Differences").mkdir(parents=True, exist_ok=True)
    print("Starting Comparison...")
    for i, j in zip([0, 1], [1, 0]):
        csv_1, csv_2 = files_to_compare[i], files_to_compare[j]
        csv_1_filename = csv_1.rstrip(".csv")
        with open(f"{csv_1}", 'r', encoding="UTF-8") as base_csv, \
            open(f"{csv_2}", 'r', encoding="UTF-8") as adjusted_csv:
            base = set(base_csv.readlines())
            adjusted = set(adjusted_csv.readlines())
        # Write the missing entries for base_csv
        with open(f".\Differences\{csv_1_filename}-Differences.csv", 'w', encoding="utf8") as differences_csv:
            differences = sorted(adjusted.difference(base))
            for line in differences:
                differences_csv.write(line)
    else:
        print("Finished Comparison.\n\n")



if __name__ == "__main__":
    main()