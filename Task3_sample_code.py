import lmql
import asyncio
import json
import os


async def query(prompt):
    output = (await lmql.run(prompt, output_writer=lmql.stream("RESPONSE")))
    return output

if __name__ == "__main__":
    json_name = '/home/jzhao5793/proj/modulus-magnus-linguae/sample_answers_Task3.json'
    with open(json_name, 'r') as f:
        data = json.load(f)
    stuffs=data["stuff"]
    for q in stuffs:
        for codes in q["code"]:
            response = asyncio.run(query(codes))
            prompt_from_Output = response[0].prompt
            answer_from_Output = response[0].variables['ANSWER']
            a += match_test(prompt_from_Output, answer_from_Output, json_name)
            b += 1
            print(prompt_from_Output, answer_from_Output)
    accu_rate = [a/b, b]
    print(accu_rate)

def match_test(prompt, answer, file_name):
    questions = data["stuff"]

    for q in questions:
      for prompt_in_Json in q["prompt"]:
        if prompt_in_Json in prompt:
            print("in")
            if answer == q["answer"]:
                return 1
    # If no matches were found, return 0
    return 0

print(match_test(prompt_from_Output, answer_from_Output, json_name))
