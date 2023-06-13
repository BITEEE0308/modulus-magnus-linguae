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

    folder_path = Path(args.folder_path)

    styles = ["style" + str(i) for i in range(1, 10)]
    fine_tune_folder_path = folder_path.parent / 'Ch5_A_Fine_Tune_Method3'
    os.makedirs(fine_tune_folder_path, exist_ok=True)

    for style_to_exclude in styles:
        testing_folder_path = folder_path.parent / (folder_name + "_Testing_Method3_" + style_to_exclude)
        if testing_folder_path.exists():
            shutil.rmtree(testing_folder_path)
        os.makedirs(testing_folder_path)

        training_file_path = fine_tune_folder_path / f"quiz_training_{style_to_exclude}.jsonl"
        with open(training_file_path, "w") as outfile:
            for file_path in glob.glob(f"{folder_path}/*.json"):
                file_path = Path(file_path)
                
                if "CAPITVLVM_V." in file_path.name:
                    info_list = file_path.stem.split(".")
                    fingerprint = ".".join([info_list[0], info_list[1], info_list[3]])

                    if style_to_exclude not in file_path.name:
                        with file_path.open(mode='r', encoding="utf-8") as f:
                            data = json.load(f)
                            transformed_data = [
                                {
                                    'prompt': re.search(r"'(.*?)' from", entry['code']).group(1).removesuffix(' [ANSWER]'),
                                    'completion': entry['answer']
                                }
                                for entry in data['codes']
                            ]

                            for entry in transformed_data:
                                json.dump(entry, outfile)
                                outfile.write('\n')
                    else:
                        shutil.copy(file_path, testing_folder_path / file_path.name)
                else:
                    shutil.copy(file_path, testing_folder_path / file_path.name)

if __name__ == "__main__":
    main()

