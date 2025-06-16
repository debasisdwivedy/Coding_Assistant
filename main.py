import os, json
from dotenv import load_dotenv
from openai import OpenAI
from argparse import ArgumentParser
from toolschema import ToolSchema
from prompts import SYSTEM_PROMPT
from functions.call_function import call_function

parser = ArgumentParser(description="AI Agent interface")
parser.add_argument("question",help="The action that you want the agent to perform")
parser.add_argument("--verbose",help="Verbose",action='store_true',default=False,required=False)
args = parser.parse_args()

load_dotenv()
VERBOSE = args.verbose
question = args.question
FINAL_RESPONSE = True
MAX_STEPS_ALLOWED = 20
INPUT_TOKENS_USED = 0
OUTPUT_TOKENS_USED = 0
TOTAL_TOKENS_USED = 0
TOTAL_NUMBER_OF_STEPS = 0

client = OpenAI(
    api_key=os.environ.get("OPENAI-API-KEY"),
)

messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": question,
        }
    ]

while FINAL_RESPONSE and MAX_STEPS_ALLOWED > 0:
    MAX_STEPS_ALLOWED -= 1
    TOTAL_NUMBER_OF_STEPS += 1
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=[ToolSchema.LIST_FOLDER_SCHEMA.value, ToolSchema.GET_FILE_CONTENT_SCHEME.value, ToolSchema.WRITE_FILE_SCHEMA.value, ToolSchema.RUN_PYTHON_FILE_SCHEMA.value],
    )

    if response.usage.prompt_tokens is not None:
        INPUT_TOKENS_USED += int(response.usage.prompt_tokens)
    if response.usage.completion_tokens is not None:
        OUTPUT_TOKENS_USED += int(response.usage.completion_tokens)
    if response.usage.total_tokens is not None:
        TOTAL_TOKENS_USED += int(response.usage.total_tokens)

    tool_calls = response.choices[0].message.tool_calls

    if tool_calls is None or len(tool_calls) <= 0:
        FINAL_RESPONSE = False
        messages.append({"role": "assistant", "content": response.choices[0].message.content})
    else:
        #print("=======================TOOL CALLS===========================")
        #messages.append(response.choices[0].message)
        messages.append({"role": "assistant", "tool_calls": tool_calls})
        for tool_call in tool_calls:
            function_name = tool_call.function.to_dict()['name']
            argument = json.loads(tool_call.function.to_dict()['arguments'])
            function_result = call_function(function_name,argument,verbose=VERBOSE)
            tool_response = {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(function_result)
            }
            # print(f"-> {function_result}")
            #print(f"Function call result is: {function_result}")
            messages.append(tool_response)
        #print("===============================================================")

print("=======================FINAL TEXT RESPONSE===========================\n")
#print(response.output_text)
print(messages[-1]["content"])
print("===============================================================\n")

if VERBOSE:
    print("==========================FINAL RESPONSE OBJECT=============================\n")
    print(response)
    print("============================================================================\n")
    print("========================ALL MESSAGES=============================================\n")
    for i,message in enumerate(messages):
        if "role" in message:
            print(f"{i}. {message['role']}: {message}")
        else:
            print(f"{i}. Undefined: {message}")
    print("=================================================================================\n")
    print(f"User prompt: {question}")
    print(f"Prompt tokens: {INPUT_TOKENS_USED}")
    print(f"Response tokens: {OUTPUT_TOKENS_USED}")
    print(f"Total tokens: {TOTAL_TOKENS_USED}")
    print(f"Total number of steps: {TOTAL_NUMBER_OF_STEPS}")
