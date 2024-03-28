# pandas for csv handling
import pandas as pd
# fileinput for find and replace
import fileinput
# cl arguments
import argparse
import os
import time 

delimiter = ','

parser = argparse.ArgumentParser()
parser.add_argument('--classes_mapping', default='classes_mapping.csv', help='Input classes mapping from old to new. Default: classes_mapping.csv')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-f','--file', help='Input filename path.')
group.add_argument('-d','--directory', help='Input directory.')

args = parser.parse_args()
csv_output = args.classes_mapping
file_in = args.file if args.file != '' else None
dir_in = args.directory if args.directory != '' else None

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
    with fileinput.FileInput(replace_input, inplace=True) as file:
        for line in file:
            for class_old, class_new in replace_dict:
                line = line.replace(class_old, class_new)
            # write the modified line to file
            print(line, end='')

if __name__ == "__main__":
    start_time = time.time()
    print(file_in, dir_in)
    if file_in:
        find_and_replace(csv_output, file_in)
    elif dir_in:
        for subdir, _, files in os.walk(dir_in):
            for file in files:
                file_path = os.path.join(subdir, file)
                print("Processing: ", file_path)
                find_and_replace(csv_output, file_path)
    print(f'--- {time.time() - start_time} seconds ---')