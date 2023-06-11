import json
import re
from pathlib import Path
import argparse
import glob
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder_path')
    args = parser.parse_args()

    folder_name = args.folder_path

    folder_path = Path(args.folder_path)

    testing_folder_path = folder_path.parent / (folder_name + "_Testing")

    if testing_folder_path.exists():
        shutil.rmtree(testing_folder_path)
    os.makedirs(testing_folder_path)

    processed_files = set()

    # iterate over all json files in the given directory
    for file_path in glob.glob(f"{folder_path}/*.json"):
        file_path = Path(file_path)
        info_list = file_path.stem.split(".")
        fingerprint = ".".join([info_list[0], info_list[1], info_list[3]])

        if fingerprint not in processed_files:
            processed_files.add(fingerprint)
            with file_path.open(mode='r', encoding="utf-8") as f:
                data = json.load(f)
                transformed_training_data = [
                    {
                        'prompt': re.search(r"'(.*?)' from", entry['code']).group(1).removesuffix(' [ANSWER]'),
                        'completion': entry['answer']
                    }
                    for entry in data['codes'][:5]
                ]

                transformed_testing_data = [
                    {
                        'prompt': re.search(r"'(.*?)' from", entry['code']).group(1).removesuffix(' [ANSWER]'),
                        'completion': entry['answer']
                    }
                    for entry in data['codes'][5:]  # get all items starting from the 6th
                ]
            
            with open(f"quiz_training_data.jsonl", "a") as outfile:
                for entry in transformed_training_data:
                    json.dump(entry, outfile)
                    outfile.write('\n')

            with open(f"quiz_testing_data.jsonl", "a") as outfile:
                for entry in transformed_testing_data:
                    json.dump(entry, outfile)
                    outfile.write('\n')

            testing_file_path = testing_folder_path / file_path.name
            with open(testing_file_path, "w") as outfile:
                json.dump({"codes": data['codes'][5:]}, outfile)


if __name__ == "__main__":
    main()

