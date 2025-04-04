import os
import json
import requests
import time
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview"
)

assistant = client.beta.assistants.create(
    model="gpt-4o", 
    instructions="",
    tools=[{"type":"file_search"},{"type":"code_interpreter"},{"type":"function","function":{"name":"get_preferred_answer","description":"從 Google Sheet 的常見問答中找出最接近的問題","parameters":{"type":"object","properties":{"query":{"type":"string","description":"使用者提出的問題"}},"required":["query"]}}}],
    tool_resources={"file_search":{"vector_store_ids":[]},"code_interpreter":{"file_ids":[]}},
    temperature=1,
    top_p=1
)

# Create a thread
thread = client.beta.threads.create()

# Add a user question to the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="hi" # Replace this with your prompt
)



# Run the thread
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Looping until the run completes or fails
while run.status in ['queued', 'in_progress', 'cancelling']:
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
)

if run.status == 'completed':
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print(messages)
elif run.status == 'requires_action':
    # the assistant requires calling some functions
    # and submit the tool outputs back to the run
    pass
else:
    print(run.status)