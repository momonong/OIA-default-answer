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
    user_question = "我是僑生，新生體檢多少錢甚麼時候?"
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_question
    )

    # 啟動 assistant 運行
    run = client.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=assistant.id
    )

    # 等待 assistant 完成或進入 tool call 階段

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        if run.status in ["queued", "in_progress"]:
            print("in progress")
            time.sleep(1)

        elif run.status == "requires_action":
            print("required action")
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for call in tool_calls:
                tool_outputs.append(handle_tool_call(call))

            # 回傳工具執行結果
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
            )
            time.sleep(1)

        elif run.status == "completed":
            print("tool end")
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for m in messages.data[::-1]:
                if m.role == "assistant":
                    print("\n🤖 Assistant 回覆：")
                    print(m.content[0].text.value)
            break

        else:
            print(f"⚠️ Unexpected run status: {run.status}")
            break


if __name__ == "__main__":
    main()