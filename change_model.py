import json
import glob
import re
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder_path')
    parser.add_argument('replace_model')
    args = parser.parse_args()

    folder_path = Path(args.folder_path)
    replace_model = args.replace_model

    for file_path in glob.glob(f"{folder_path}/*.json"):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for entry in data.get('codes', []):
            code = entry.get('code', '')
            entry['code'] = re.sub(rf'from\s\'(.+?)\'\swhere', f'from \'openai/{replace_model}\' where', code)
        new_file_path = str(file_path).replace('text-ada-001', replace_model)
        with open(new_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        if file_path != new_file_path:
            Path(file_path).unlink()

if __name__ == "__main__":
    main()

