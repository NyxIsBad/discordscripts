import csv
import re

# Define the input and output filenames
diff_input = 'classesjs.diff'
csv_output = 'classes_mapping.csv'

# Match all inside brackets
bracket_isolating = r'{([^}]*)}'
info_isolating = r'^(-|\+)\s*(.*):\s*"(.*)"$'

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
            if class_id not in old_dict:
                # similarly with col1 with new classes
                writer.writerow(['$NOTFOUND$', new_dict[class_id], class_id])
        break