import glob
import os

class_file = open('classlist.txt', 'r')
src_file = open('csssource10.css','r')
sp = src_file.read()

dp = class_file.read()
da = dp.split()

fail = []

for cl in da:
    print(f"Checking {cl}")
    if not cl in sp:
        fail.append(cl)

with open('fail.txt','w') as out:
    out.write('\n'.join(str(cl) for cl in fail))

