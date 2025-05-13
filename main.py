from src.clients.assistant_client import init_client
from src.classes.agent import Agent


def main():
    # 初始化 client 和建立 thread
    client = init_client()
    thread = client.beta.threads.create()

    # 初始化 Agent（只需要做一次）
    assistant_id = "asst_xxxxxxxxxxxxxxxxxxxxxxxx"  # 請替換成您的 assistant ID
    agent = Agent(assistant_id)

    # 模擬使用者提問
    user_question = "我是僑生，新生體檢多少錢甚麼時候?"
    
    # 使用 chat 方法獲取回答
    answer = agent.chat(thread.id, user_question)
    print("\n🤖 Assistant 回覆：")
    print(answer)


if __name__ == "__main__":
    main()