import json
import re
from pathlib import Path
import argparse
import glob
import os
import shutil

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder_path')
    args = parser.parse_args()

    folder_name = args.folder_path
    print(folder_name)

    if os.path.exists(f'training_testing_{folder_name}'):
        shutil.rmtree(f'training_testing_{folder_name}')
    os.makedirs(f'training_testing_{folder_name}')

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
            
            json_name = ".".join([info_list[0], info_list[1], info_list[3]])
            with open(f"training_testing_{folder_name}/{json_name}.jsonl", "w") as outfile:
                for entry in transformed_data:
                    json.dump(entry, outfile)
                    outfile.write('\n')

if __name__ == "__main__":
    main()

