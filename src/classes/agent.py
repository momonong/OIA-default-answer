from src.clients.assistant_client import init_client
from src.app.tool_handler import handle_tool_call
import time


class Agent:
    def __init__(self, assistant_id: str):
        self.client = init_client()
        self.assistant_id = assistant_id

    def chat(self, thread_id: str, user_query: str) -> str:
        """
        處理單次對話
        
        Args:
            thread_id: 對話的 thread ID
            user_query: 使用者的問題
            
        Returns:
            str: Assistant 的回答
        """
        # 添加使用者訊息
        self.client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=user_query
        )

        # 啟動 assistant 運行
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=self.assistant_id
        )

        # 等待 assistant 完成或進入 tool call 階段
        while True:
            run = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

            if run.status in ["queued", "in_progress"]:
                time.sleep(1)

            elif run.status == "requires_action":
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []

                for call in tool_calls:
                    tool_outputs.append(handle_tool_call(call))

                # 回傳工具執行結果
                self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id, run_id=run.id, tool_outputs=tool_outputs
                )
                time.sleep(1)

            elif run.status == "completed":
                messages = self.client.beta.threads.messages.list(thread_id=thread_id)
                for m in messages.data[::-1]:
                    if m.role == "assistant":
                        return m.content[0].text.value

            else:
                raise Exception(f"⚠️ Unexpected run status: {run.status}")


if __name__ == "__main__":
    # 初始化 client 和建立 thread
    client = init_client()
    thread = client.beta.threads.create()
    
    # 初始化 Agent，只需要傳入 assistant_id
    assistant_id = "asst_xxxxxxxxxxxxxxxxxxxxxxxx"  # 請替換成您的 assistant ID
    agent = Agent(assistant_id)
    
    # 使用 chat 方法獲取回答
    user_question = "我是僑生，新生體檢多少錢甚麼時候?"
    answer = agent.chat(thread.id, user_question)
    print("\n🤖 Assistant 回覆：")
    print(answer)
