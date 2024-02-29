# regex and csv handling
import csv
import re
# pandas for csv handling
import pandas as pd
# tqdm for progress bar
from tqdm import tqdm
# fileinput for find and replace
import fileinput
# cl arguments
import argparse

# ----------------- GLOBAL VARS -----------------
# Create argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--input', default='classesjs.diff', help='Input filename. Default: classesjs.diff')
parser.add_argument('--output', default='classes_mapping.csv', help='Output filename. Default: classes_mapping.csv')
parser.add_argument('--diff_output', default=None, help='Generate diff file. Input a file name. Default: None')
parser.add_argument('--syndi', default=False, help='Decide whether or not to format the diff_output as a SyndiShanX input file. Default: False')
parser.add_argument('--replace', default=None, help='Auto Update a file. Input a file name. Default: None')

# Parse command line arguments
args = parser.parse_args()

# Get input and output filenames from command line arguments
diff_input = args.input
csv_output = args.output
diff_output = args.diff_output
flag_syndi = args.syndi
replace_input = args.replace

# Function relevant vars
# Delimiter for csv interpretation
delimiter = ','
# Match all inside brackets
bracket_isolating = r'{([^}]*)}'
# Fetch elements of field
info_isolating = r'^(-|\+)\s*(.*):\s*"(.*)"$'

# ----------------- FUNCTIONS -----------------
# load a csv file into a pandas dataframe
def load_csv(input):
    data = pd.read_csv(input, sep=delimiter, header=0, keep_default_na=False)
    return data # returns df
# parse a diff file and write the differences to a csv file
def parse_diff():
    # read file
    with open(diff_input, 'r') as f:
        content = f.read()

    # find all matches
    matches = re.findall(bracket_isolating, content)

    # open the csv file; we open it now instead of later so we can write the header
    with open(csv_output, 'w', newline='') as csvfile:
        # declare io obj and write header
        writer = csv.writer(csvfile)
        writer.writerow(['class_old', 'class_new', 'id'])
        # Extract old and new classes for each match using the id field as a reference
        for match in matches:
            # Declare vars, note that dicts reset every match
            old_dict = {}
            new_dict = {}
            # Split each match by commas
            fields = [field.strip() for field in match.split(',')]
            # Extract id and class for each field
            for field in fields:
                if field:
                    matchobj = re.match(info_isolating,field)
                    # ensure that our match is complete
                    if matchobj and len(matchobj.groups()) == 3:
                        prefix, class_id, class_selector = matchobj.groups()
                        if prefix == "-":
                            old_dict[class_id] = class_selector
                        elif prefix == "+":
                            new_dict[class_id] = class_selector
            # write the differences to the csv
            for class_id in old_dict:
                # we need to split the class_selector according to " "
                old_selector_arr = old_dict[class_id].split(" ")
                # case it's in the new dict
                if class_id in new_dict:
                    new_selector_arr = new_dict[class_id].split(" ")
                    for i in range(len(old_selector_arr)):
                        # we compare the selectors and write the differences
                        if old_selector_arr[i] != new_selector_arr[i]:
                            writer.writerow([old_selector_arr[i], new_selector_arr[i], class_id])
                # case possibly deleted class
                else:
                    for i in range(len(old_selector_arr)):
                        writer.writerow([old_selector_arr[i], '$NOTFOUND$', class_id])
            for class_id in new_dict:
                new_selector_arr = new_dict[class_id].split(" ")
                if class_id not in old_dict:
                    for i in range(len(new_selector_arr)):
                        writer.writerow(['$NOTFOUND$', new_selector_arr[i], class_id])

def diff():
    # load csv to df
    df = load_csv(csv_output)
    # open the diff file
    with open(diff_output, 'w') as f:
        # make check here instead of later for efficiency
        if flag_syndi:
            for index, row in df.iterrows():
                if row['class_old'] != '$NOTFOUND$' and row['class_new'] != '$NOTFOUND$':
                    f.write(f"{row['class_old']}\n{row['class_new']}\n")
        else:
            for index, row in df.iterrows():
                if row['class_old'] != '$NOTFOUND$' and row['class_new'] != '$NOTFOUND$':
                    f.write(f"-{row['class_old']}\n+{row['class_new']}\n")

def find_and_replace():
    # load csv to df
    df = load_csv(csv_output)
    replace_dict = dict(zip(df['class_old'], df['class_new']))
    # count lines for progress bar lol
    with open(replace_input, 'r') as file:
        total_lines = sum(1 for _ in file)
    # we're just gonna brute force it
    with fileinput.FileInput(replace_input, inplace=True, backup=".bak") as file:
        # progress bar!
        with tqdm(total=total_lines, desc="Replacing") as pbar:
            for line in file:
                for class_old, class_new in replace_dict.items():
                    if class_old != '$NOTFOUND$' and class_new != '$NOTFOUND$':
                        line = line.replace(class_old, class_new)
                # write the modified line to file
                print(line, end='')
                pbar.update(1)


def main():
    parse_diff()
    if diff_output:
        diff()
    if args.replace:
        find_and_replace()

# driver code
if __name__ == "__main__":
    main()