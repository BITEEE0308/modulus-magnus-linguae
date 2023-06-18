import os
import json
import csv
from collections import defaultdict
import argparse

# set up accumulators for each method type
totals = defaultdict(int)
counts = defaultdict(int)

# setup command line argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('folder_path')
args = parser.parse_args()

# specify your directory here
folder_path = args.folder_path

# iterate through each json file in the directory
for file in os.listdir(folder_path):
    if file.endswith(".json") and 'method' in file:

        # extract method type from the filename
        method = file.split('.')[2].split('_')[1]
        print(method)

        # load the json file which contains a single number
        with open(os.path.join(folder_path, file)) as json_file:
            number = json.load(json_file)
            totals[method] += number
            counts[method] += 1

# calculate the averages
averages = {method: total / counts[method] for method, total in totals.items()}

# write to csv
with open('averages.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Method', 'Average'])
    for method, average in averages.items():
        writer.writerow([method, average])

