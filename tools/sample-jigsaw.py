# The point of this tool is to cache a subset of the full jigsaw dataset.

import csv

subset_size = 500

input_file_path = "data/full/data-jigsaw.csv"
output_file_path = "data/test-big/data-jigsaw-500.csv"

with (
    open(input_file_path, mode="r") as input_file,
    open(output_file_path, mode="w") as output_file,
):
    csvFileIn = csv.reader(input_file)
    csvFileOut = csv.writer(output_file)

    header = next(csvFileIn)
    csvFileOut.writerow(header)

    rows_processed = 0
    for line in csvFileIn:
        if rows_processed < subset_size:
            csvFileOut.writerow(line)
            rows_processed += 1
        else:
            break

    print(
        f"Subset of size {rows_processed} from {input_file_path} written to {output_file_path}"
    )
