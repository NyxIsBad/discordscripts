import csv
import sys

def generate_csv(diff_file, csv_file):
    changes = []
    with open(diff_file, 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 2):
            if i+1 < len(lines):
                if lines[i].startswith('-') and lines[i+1].startswith('+'):
                    changes.append((lines[i][1:].strip(), lines[i+1][1:].strip()))
                else:
                    print("Error: Invalid format detected. Exiting.")
                    print("Line 1: " + lines[i])
                    print("Line 2: " + lines[i+1])
                    sys.exit(1)
            else:
                print("Error: Incomplete change detected. Exiting.")
                sys.exit(1)

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['class_old', 'class_new'])
        writer.writerows(changes)
    print("CSV file generated successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.diff output.csv")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    generate_csv(input_file, output_file)
