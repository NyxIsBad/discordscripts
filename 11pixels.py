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

def parse_diff():
    with open("11pixels.txt",'r') as fin, open("11pixels.csv",'w') as fcsvout, open("11pixels.diff",'w') as fdiffout:
        while True:
            line1 = fin.readline().strip()
            line2 = fin.readline().strip()

            if not line1 and not line2:
                break

            if (line1 != "__MISSINGNO__" and "/" not in line1 and "\\" not in line1 and
            line2 != "__MISSINGNO__" and "/" not in line2 and "\\" not in line2):
                
                fcsvout.write(f"{line1},{line2}\n")
                fdiffout.write(f"-{line1}\n+{line2}\n")
        

parse_diff()