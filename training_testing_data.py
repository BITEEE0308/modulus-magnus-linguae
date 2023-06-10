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
    print(folder_name)

    folder_path = Path(args.folder_path)
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
                transformed_data = [
                    {
                        'prompt': re.search(r"'(.*?)' from", entry['code']).group(1).removesuffix(' [ANSWER]'),
                        'completion': entry['answer']
                    }
                    for entry in data['codes']
                ]
            
            # change the file path to a fixed path
            with open(f"all_quiz_data.jsonl", "a") as outfile:
                for entry in transformed_data:
                    json.dump(entry, outfile)
                    outfile.write('\n')

if __name__ == "__main__":
    main()

