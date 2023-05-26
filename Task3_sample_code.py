import lmql
import asyncio
import json
import os
import sys

async def query(prompt):
    output = (await lmql.run(prompt, output_writer=lmql.stream("RESPONSE")))
    return output

def match_test(code, answer, file_name):
    codes = data["codes"]
    for c in codes:
        if code == c["code"]:
            if answer == c["answer"]:
                return 1
    return 0

def main(filename):
    codes=data["codes"]
    a = 0
    b = 0
    for c in codes:
            response = asyncio.run(query(c["code"]))
            answer_from_Output = response[0].variables['ANSWER']
            a += match_test(c, answer_from_Output, data)
            b += 1
    accu_rate = a/b
    return accu_rate

if __name__ == "__main__":
    print(len(sys.argv))
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    main(data)
