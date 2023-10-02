# Generate and Compare CSV

The `generate-compare.py` script walks through the drive or path specified and looks for the file exts specified. It writes the path of where the file is stored, and the name of the file into a CSV `(path, file)`. After the generation has been completed, it will compare the files that have the same folder name but different drive letter. It will dump the differences into a CSV.

The `compare.py` script searches your current working directory for any existing CSV files; If there are only 2 CSV files, it will automatically compare them for you. If there are more than 2 CSV files, you will be given the option to choose which 2 files you want to compare.

## Intended File Structure for `generate-compare.py`

``` file

Drive:\
+---Folder A
|   +---...
|   ...
+---Folder B
|   +---...
|   ...
+---Folder C
|   +---...
|   ...
...

```

## .bat file

The script was made with the intention of running it via a Windows batch file.

``` bat

@py.exe "PATH\TO\generate-compare.py" %*
@pause

```
