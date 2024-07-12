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

# ----------------- GLOBAL VARS -----------------
parser = argparse.ArgumentParser()
parser.add_argument('--input', default='1.js', help='Input filename. Default: 1.js')
# Parse command line arguments
args = parser.parse_args()

js_input = args.input

bracket_isolating = r'= {([^}]*)}'


def parse():
    with open(js_input, 'r') as f:
        print("File opened\n")
        content = f.read()
    print("Content read\n")
    matches = re.findall(bracket_isolating, content)
    # Write matches to a file
    with open('testmatches.txt', 'w') as f:
        for match in matches:
            f.write(match + '\n')
            print(match)

def sort_lines_within_braces(text):
    # Define the regex pattern to match content between { and }
    pattern = re.compile(bracket_isolating, re.DOTALL)

    def process_lines(lines):
        result = []
        for i, line in enumerate(lines):
            if i < len(lines) - 1:  # Not the last element
                if not line.endswith(','):
                    line += ','
            else:  # Last element
                if line.endswith(','):
                    line = line[:-1]  # Remove the trailing comma
            result.append(line)
        return result
    # Function to sort lines within each matched block
    def sort_block(match):
        # Extract the block content, split by lines, and strip leading/trailing spaces
        block_content = match.group(1).strip().split('\n')
        # Sort the lines
        sorted_content = process_lines(sorted(line.strip() for line in block_content if line.strip()))
        # Join the sorted lines with newline and wrap with braces
        
        return '= {\n            ' + '\n            '.join(sorted_content) + '\n        }'

    # Use re.sub to replace each match with sorted content
    sorted_text = pattern.sub(sort_block, text)
    return sorted_text

def sort_file_in_place(filename):
    # Read the content of the file
    with open(filename, 'r') as file:
        content = file.read()

    # Sort the lines within braces
    sorted_content = sort_lines_within_braces(content)

    # Write the modified content back to the file
    with open(filename, 'w') as file:
        file.write(sorted_content)

sort_file_in_place(js_input)