# Generate and Compare CSV

This script walks through the parent folders in your drives and uses the parent folder names as a base for comparison. From there, it will compare the files within the folders. Finally, it will output a CSV file that reflects the differences.

## .bat file

The script was made with the intention of running it via a Windows batch file.

``` bat

@py.exe "PATH\TO\generate-compare.py" %*
@pause

```
