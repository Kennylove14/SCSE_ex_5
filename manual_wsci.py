from pathlib import Path
from ollama import chat


question = """
I changed my university password this morning.
Now my Windows laptop won't connect to campus Wi-Fi,
but my phone still works.
"""

selected_files = [
    ##Use only the files that are relevant to the question.
    "knowledge/password_changes.txt",
    "knowledge/wifi_setup.txt",
    "knowledge/service_status.txt"
]


context = ""

## Write a for loop to go through all the files in selected_files and read their contents into the context variable.
for file_path in selected_files:
    context += Path(file_path).read_text()
    context += "\n\n"

## Call Qwen with the student's question and the context you created above.
response = chat(
    model="qwen",
    messages=[
        {"role": "system", "content": f"Answer the user's question using only the information from the provided context:\n\n{context}"},
        {"role": "user", "content": question}
    ]
)


print(
    "Context characters:",
    len(context)
)
print(response.message.content)