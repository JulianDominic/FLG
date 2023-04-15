# Generate and Compare CSV
## file_list_generators.py
The first script `file_list_generators.py` is used to walk through the target directory and generate a CSV that keeps track of the child files.

Each row in the output CSV will be in the format of `Folder Path` and `File Name`.

## compare_csv.py
The second script `compare_csv.py` is used to find the differences in the entries of two different CSVs then it will create a CSV with the differences.

Each row in the output CSV will also be in the format of `Folder Path` and `File Name`.s

## .bat file
These two scripts were made with the intention of running them via a Windows batch file.
For example:
```bat
@py.exe "PATH\TO\compare_csv.py" %*
@pause
```