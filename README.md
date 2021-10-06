Converts Swissborg account statement files to Coinstat CSV format.

In the Swissborg app, export your account statement in Excel format. The script accepts `xlsx` files, however the `openpyxl` module is then required in your Python environment. You can install it with `pip install openpyxl`. Otherwise, just open the `xlsx` file with Excel  then save as a CSV.

To convert your account statement file, simply run the script as follow:

```
python sb2cs source_file destination_file.csv
```

where `source_file` will be a CSV or `xlsx` file and `destination_file.csv` is the name of the file you'll import to Coinstat.

## Example
An example file, in CSV format is provided so that you can test the script.

## Issues?
If you encounter any issue, it is either due to your Python environment or due to corner cases in the transactions file that are not taken into account.

To make things simple, the script only requires Python 3.x, `numpy`, `pandas` and optionally `openpyxl`.

In case you're having issues coming from the transactions themselves, try to isolate the problematic line and check if that case is included in the example file. If that's not the case, kindly open an issue.
