import time
from src.clients.assistant_client import init_client, init_assistant
from src.app.tool_handler import handle_tool_call


def main():
    # 初始化 Azure client
    client = init_client()
    # 建立 Assistant（只需執行一次）
    assistant = init_assistant(client)
    # 建立對話 thread
    thread = client.beta.threads.create()

    # 模擬使用者提問
    user_question = "申請復學的居留簽證的時候需要的復學證明可以什麼時候拿到?"
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_question
    )

    # 啟動 assistant 運行
    run = client.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=assistant.id
    )

    # 等待 assistant 完成或進入 tool call 階段
    while run.status in ["queued", "in_progress"]:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Assistant 要求呼叫工具
    if run.status == "requires_action":
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        tool_outputs = []

        for call in tool_calls:
            tool_outputs.append(handle_tool_call(call))

        # 回傳工具執行結果
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
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


if __name__ == "__main__":
    main()

# # Create a thread
# thread = client.beta.threads.create()

# # Add a user question to the thread
# message = client.beta.threads.messages.create(
#     thread_id=thread.id,
#     role="user",
#     content="hi" # Replace this with your prompt
# )


# # Run the thread
# run = client.beta.threads.runs.create(
#     thread_id=thread.id,
#     assistant_id=assistant.id
# )

# # Looping until the run completes or fails
# while run.status in ['queued', 'in_progress', 'cancelling']:
#     time.sleep(1)
#     run = client.beta.threads.runs.retrieve(
#     thread_id=thread.id,
#     run_id=run.id
# )

# if run.status == 'completed':
#     messages = client.beta.threads.messages.list(
#         thread_id=thread.id
#     )
#     print(messages)
# elif run.status == 'requires_action':
#     # the assistant requires calling some functions
#     # and submit the tool outputs back to the run
#     pass
# else:
#     print(run.status)
