from pathlib import Path
from ollama import chat
import json



question = """
I changed my university password this morning.
Now my Windows laptop won't connect to campus Wi-Fi,
but my phone still works.
"""

## WRITE ##
service_status = {
    "wifi": "operational"
}

state = {
    "problem": question,
    "wi_fi status": "operational",
    "wi-fi_check": True
}

with open("state.json", "w") as file:
    json.dump(
        state,
        file,
        indent=2
    )

with open("state.json", "r") as file:
    state = json.load(file)

print(state)


## SELECT CONTEXT FILES BASED ON QUESTION
## Create the function that takes the student's question, takes some keywords and chooses the relevant files from the knowledge base. Return a list of the selected files.
## For example, if the question has the kyeword "print" or "printer", then the function should return the file "knowledge/printer_setup.txt" in a list.
def select_context(question):
    keyword_map = {
        "wifi": ["knowledge/wifi_setup.txt", "knowledge/service_status.txt"],
        "wi-fi": ["knowledge/wifi_setup.txt", "knowledge/service_status.txt"],
        "password": ["knowledge/password_changes.txt"],
        "email": ["knowledge/email_setup.txt"],
        "print": ["knowledge/printing.txt"],
        "printer": ["knowledge/printing.txt"],
        "vpn": ["knowledge/vpn.txt"],
        "projector": ["knowledge/classroom_projectors.txt"],
        "display": ["knowledge/classroom_projectors.txt"]
    }
    
    question_lower = question.lower()
    selected = set()
    
    for keyword, files in keyword_map.items():
        if keyword in question_lower:
            for f in files:
                selected.add(f)
    
    return list(selected)


selected_files = select_context(question)

## READ SELECTED FILES and add their contents to the context variable.
context = ""
for file_path in selected_files:
    context += Path(file_path).read_text()
    context += "\n\n"

## 
## COMPRESS CONTEXT
## Add logic to compress the context from above by calling Qwen with "context" and the "question" as the parameter
## The response from Qwen should be the compressed context. Store it in a variable called "compressed_context" 

def compress_context(context, question):
    prompt = f"""
Extract only the information directly relevant to answering the user's question from the context below.
Keep only key facts, troubleshooting steps and service status related to the issue.
Do not include any irrelevant content.

Context:
{context}

User Question:
{question}

Relevant extracted information:
"""
    response = chat(
        model="qwen",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.message.content.strip()

compressed_context = compress_context(context, question)


## Print the length of the compressed context
print(len(compressed_context))

## Now, call Qwen again with the compressed context and the student's question. Store the response in a variable called "response" and print the response from Qwen.
## Ensure the model produces a structured output 
answer_prompt = f"""
Use the following relevant context to answer the user's question.
Provide a structured response with:
1. Problem diagnosis
2. Root cause analysis
3. Step-by-step solution

Context:
{compressed_context}

User Question:
{question}
"""

response = chat(
    model="qwen",
    messages=[{"role": "user", "content": answer_prompt}]
)

print("\nModel response:")

print(response.message.content)

## WRITE the above output in an artifact called "state"

## Update the rest of the code so that it uses the "state" artifact as part of the context. 
## It is important to ensure that the model uses only the relevant parts from the "state" artifact and not the entire artifact.
## For this, you may have to think of a good structure for the "state" artifact and how to use it in the context.


