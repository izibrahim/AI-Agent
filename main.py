import os
from actions import connect_to_node
from prompts import system_prompt
from json_helpers import extract_json

from groq import Groq

client = Groq(api_key="Your Key")

def generate_text_with_conversation(messages, model="llama3-70b-8192"):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

def general_information(query):
    # Simple placeholder for general information queries
    predefined_responses = {
        "What is the show ip int br command and what does it do?": (
            "The 'show ip interface brief' (or 'show ip int br' for short) is a Cisco IOS command "
            "used to display a brief summary of all the interfaces on the router, including their status "
            "and IP addresses. It provides a quick and easy way to check the status of all interfaces on the router."
        )
    }
    return predefined_responses.get(query, "I don't have information on that query.")

available_actions = {
    "connect_to_node": connect_to_node,
    "general_information": general_information
}

user_prompt = "ssh to the R1 and reload the node and explain the output?"

messages = [
    {"role": "user", "content": user_prompt},
    {"role": "system", "content": system_prompt}
]

turn_count = 1
max_turns = 5
while turn_count < max_turns:
    print(f"Loop: {turn_count}")
    print("----------------------")
    turn_count += 1
    response = generate_text_with_conversation(messages, model="llama3-8b-8192")
    print(response)
    json_function = extract_json(response)

    if json_function:
        function_name = json_function[0].get('function_name')
        function_parms = json_function[0].get('function_parms', {})

        if function_name == "nothing":
            print("No further action required.")
            break

        if function_name not in available_actions:
            print(f"Unknown action: {function_name}. Skipping.")
            continue

        print(f" -- running {function_name} {function_parms}")
        action_function = available_actions[function_name]
        
        # Call the function
        result = action_function(**function_parms)
        function_result_message = f"Action_Response: {result}"
        messages.append({"role": "user", "content": function_result_message})
        print(function_result_message)
    else:
        break
