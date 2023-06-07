import os
os.environ['PYTHONASYNCIODEBUG'] = '1'
import asyncio
import lmql
import json
import sys
import csv
from pathlib import Path
import argparse
import aiometer
from functools import partial

async def query(c):
    '''takes in a dict that includes lmql prompt and the true answer,
    returns 1 if the model is correctand 0 if wrong'''
    print("making requet HEHEOOO")
    output = (await lmql.run(c["code"], output_writer=lmql.stream("RESPONSE")))
    if output[0].variables['ANSWER'].strip() == c["answer"]:
        return 1
    return 0

async def run(codes):
    results = await aiometer.run_all([partial(query,c) for c in codes], max_per_second=.2, max_at_once=5)
    return results

def calcAccuracy(codes):
    '''calculates accuracy based on outputs from query
    >>> calcAccuracy([{'code': ('argmax "Q: Fill in the missing words: Italia ~ Europa est; Graecia ~ in Europa est. '
    ...                 'Answer Choices: (A) in quoque (B) ne non (C) ubi (D) non sed '
    ...                 'A: [ANSWER]" from "openai/text-davinci-003" where ANSWER in ["A", "B","C", "D"]'),'answer': 'A'}, {'code': ('argmax' 
    ...                 '"Q: Fill in the missing words: ~ est Arabia? In Asia est Arabia. '
    ...                 'Answer Choices: (A) in quoque (B) ne non (C) ubi (D) non sed '
    ...                 'A: [ANSWER]" from "openai/text-davinci-003" where ANSWER in ["A", "B","C", "D"]'),'answer':'C'}])
    0.5
    >>> calcAccuracy([{'code': ('argmax "Q: Fill in the tilde: Italia in Europa ~. '
    ...                 'Answer Choices: (A) est (B) sunt '
    ...                 'A: [ANSWER]" from "openai/text-davinci-003" where ANSWER in ["A", "B"]'),'answer': 'A'}, {'code': ('argmax'
    ...                 '"Q: Fill in the tilde: Italia et Gallia in Europa ~. '
    ...                 'Answer Choices: (A) est (B) sunt '
    ...                 'A: [ANSWER]" from "openai/text-davinci-003" where ANSWER in ["A", "B"]'),'answer':'B'}])
    1.0
    '''
    # using query to prompt model with questions in parallel 
    loop = asyncio.get_event_loop()
    
    results = loop.run_until_complete(run(codes))
    return round(sum(results)/len(results), 2)

def main():
    # opening json file
    parser = argparse.ArgumentParser()
    parser.add_argument('second_argument')
    parser.add_argument('third_argument')
    file_path = Path.cwd()/parser.parse_args().second_argument
    with file_path.open(mode='r',encoding="utf-8") as f:
        data = json.load(f)
    print(file_path)
    infoList = file_path.stem.split(".")
    print(infoList)
    
    jsonName = ".".join([infoList[2], infoList[0], infoList[1], infoList[3],  parser.parse_args().third_argument])
    with open("results/" + jsonName + ".json", "w") as outfile:
        outfile.write(str(calcAccuracy(data["codes"])))
        print(str(calcAccuracy(data["codes"])))

if __name__ == "__main__":
    main()
