import csv
import sys

def clean_entry(entry):
    # Remove dot if it appears before the entry
    if entry.startswith('.'):
        return entry[1:]
    return entry

def combine_csv(file1, file2, output_file):
    combined_entries = set()

    # Read and combine entries from file1
    with open(file1, 'r') as f1:
        reader = csv.reader(f1)
        next(reader)  # Skip header
        for row in reader:
            combined_entries.add((clean_entry(row[0]), clean_entry(row[1])))

    # Read and combine entries from file2
    with open(file2, 'r') as f2:
        reader = csv.reader(f2)
        next(reader)  # Skip header
        for row in reader:
            combined_entries.add((clean_entry(row[0]), clean_entry(row[1])))

    # Write combined entries to the output file
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['class_old', 'class_new'])
        for entry in combined_entries:
            writer.writerow(entry)

    print("Combined CSV file generated successfully.")

def combine_csv_to_diff(file1, file2, output_file):
    combined_entries = set()

    # Read and combine entries from file1
    with open(file1, 'r') as f1:
        reader = csv.reader(f1)
        next(reader)  # Skip header
        for row in reader:
            combined_entries.add((clean_entry(row[0]), clean_entry(row[1])))

    # Read and combine entries from file2
    with open(file2, 'r') as f2:
        reader = csv.reader(f2)
        next(reader)  # Skip header
        for row in reader:
            combined_entries.add((clean_entry(row[0]), clean_entry(row[1])))

    # Write combined entries to the output .diff file
    with open(output_file, 'w') as outfile:
        for entry in combined_entries:
            outfile.write("-" + entry[0] + "\n")
            outfile.write("+" + entry[1] + "\n")

    print("Combined .diff file generated successfully.")
    return combined_entries

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python script.py file1.csv file2.csv output.csv output.diff OPTIONAL:output.txt")
        sys.exit(1)
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    csv_output = sys.argv[3]
    diff_output = sys.argv[4]
    syndi_output = sys.argv[5] if len(sys.argv) == 6 else None
    combine_csv(file1, file2, csv_output)
    entries = combine_csv_to_diff(file1, file2, diff_output)
    if syndi_output:
        with open(syndi_output, 'w') as f:
            for entry in entries:
                f.write(entry[0] + "\n" + entry[1] + "\n")
        print("Syndi output file generated successfully.")