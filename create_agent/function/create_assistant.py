from create_agent.client.assistant_client import init_client
from openai import AzureOpenAI


def create_assistant(name="Default Assistant", instructions="請幫我回答問題", tools=None, model="gpt-4") -> str:
    """
    建立 Assistant 並回傳 assistant_id
    
    Args:
        name: Assistant 名稱
        instructions: Assistant 的任務描述
        tools: 使用的工具清單（可為 None）
        model: 使用的模型名稱（預設 gpt-4）

    Returns:
        str: 建立後的 assistant_id
    """
    client: AzureOpenAI = init_client()

    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        tools=tools or [],
        model=model
    )

    print(f"✅ Assistant 已建立，assistant_id = {assistant.id}")
    return assistant.id


if __name__ == "__main__":
    # 建立 assistant 並取得其 ID
    assistant_id = create_assistant(
        name="僑生諮詢助手",
        instructions="請協助僑生回答與新生體檢、學校規定相關的問題。",
        model="gpt-4"  # 可改為 gpt-35-turbo 等
    )
