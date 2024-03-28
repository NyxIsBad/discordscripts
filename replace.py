# regex and csv handling
import csv
import re
# pandas for csv handling
import pandas as pd
# fileinput for find and replace
import fileinput
# cl arguments
import argparse
import time

delimiter = ','

parser = argparse.ArgumentParser()
parser.add_argument('--classes_mapping', default='classes_mapping.csv', help='Input classes mapping from old to new. Default: classes_mapping.csv')
parser.add_argument('--replace_input', default='../lib/selectors/selectorPlaceholders.scss', help='Input filename. Default: ../lib/selectors/selectorPlaceholders.scss')

def load_csv(input):
    data = pd.read_csv(input, sep=delimiter, header=0, keep_default_na=False)
    return data # returns df

def find_and_replace(csv_output, replace_input):
    # load csv to df
    df = load_csv(csv_output)
    # remove not found
    df = df[(df['class_old'] != '$NOTFOUND$') & (df['class_new'] != '$NOTFOUND$')]
    replace_dict = dict(zip(df['class_old'], df['class_new'])).items()
    # we're just gonna brute force it
    with fileinput.FileInput(replace_input, inplace=True, backup=".bak") as file:
        for line in file:
            for class_old, class_new in replace_dict:
                line = line.replace(class_old, class_new)
            # write the modified line to file
            print(line, end='')

if __name__ == "__main__":
    args = parser.parse_args()
    csv_output = args.classes_mapping
    replace_input = args.replace_input
    find_and_replace(csv_output, replace_input)