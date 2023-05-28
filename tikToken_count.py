import csv
import os
import tiktoken
import pandas as pd

directory = './Summer_ML_Research'

# Output file
output_file = "OpenAI_TokenCounts.csv"

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# Prepare to write the CSV file
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Language", "Token Count"])

    # Get list of files in the directory
    files = os.listdir(directory)
    
    for file in files:
        if file == ".DS_Store":
            continue
        file_path = os.path.join(directory, file)
        try:
            with open(file_path, 'r', encoding='utf-8') as txt_file:
                text = txt_file.read()
                tokens = num_tokens_from_string(text, "cl100k_base")
                language = file[:-4]
                writer.writerow([language, tokens])
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin1') as txt_file:
                text = txt_file.read()
                tokens = num_tokens_from_string(text, "cl100k_base")
                language = file[:-4]
                writer.writerow([language, tokens])

df = pd.read_csv(output_file)
df = df.sort_values('Language')
df.to_csv(output_file, index=False)
