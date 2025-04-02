import os
import time
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from src.functions.preferred_answer import load_google_sheet, get_preferred_answer

load_dotenv()

# 初始化 Azure Assistant client
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)
client = AzureOpenAI(
    azure_ad_token_provider=token_provider,
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

# 建立 Assistant（只需執行一次）
assistant = client.beta.assistants.create(
    model="gpt-4o",
    name="QA Matcher Assistant",
    instructions="請根據使用者的問題，自動從 FAQ 中找出最接近的回答",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_preferred_answer",
                "description": "從 Google Sheet 的常見問答中找出最接近的問題",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "使用者提出的問題"
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    ]
)

# 建立對話 thread
thread = client.beta.threads.create()

# 模擬使用者提問
user_question = "申請復學的居留簽證的時候需要的復學證明可以什麼時候拿到?"
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_question
)

# 啟動 assistant 運行
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# 等待 assistant 完成或進入 tool call 階段
while run.status in ['queued', 'in_progress']:
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

# Assistant 要求呼叫工具
if run.status == "requires_action":
    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    tool_outputs = []

    for call in tool_calls:
        if call.function.name == "get_preferred_answer":
            args = json.loads(call.function.arguments)
            data = load_google_sheet()
            answer = get_preferred_answer(args["query"], data)
            tool_outputs.append({
                "tool_call_id": call.id,
                "output": answer or "查無匹配"
            })

    # 回傳工具執行結果
    client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=tool_outputs
    )

    # 再次拉結果
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

# 最終取得回覆
if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for m in messages.data[::-1]:
        if m.role == "assistant":
            print("\n🤖 Assistant 回覆：")
            print(m.content[0].text.value)
