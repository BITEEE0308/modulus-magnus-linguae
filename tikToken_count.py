import csv
import os
import tiktoken

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
        file_path = os.path.join(directory, file)
        with open(file_path, 'r', encoding='latin1') as txt_file:
            text = txt_file.read()
            tokens = num_tokens_from_string(text, "cl100k_base")
            language = file.rstrip('.txt')
            writer.writerow([file, tokens])
