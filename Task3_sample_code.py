import lmql
import asyncio
import json
import os


async def query(prompt):
    output = (await lmql.run(prompt, output_writer=lmql.stream("RESPONSE")))
    return output
def match_test(code, answer, file_name):
    codes = data["code"]
    for c in codes:
        if answer == c["answer"]:
            return 1
    return 0

def main(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    codes=data["code"]
    a = 0
    b = 0
    for c in codes:
        response = asyncio.run(query(c))
        answer_from_Output = response[0].variables['ANSWER']
        a += match_test(c, answer_from_Output, data)
        b += 1
    accu_rate = a/b
    return accu_rate

if __name__ == "__main__":
    main(sys.argv[1])
