import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


def init_client():
    """
    初始化 Azure client
    """
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_GPT41MINI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_GPT41MINI_API_KEY"),
        api_version="2024-12-01-preview",
    )
    return client


def get_model_response(question: str, answer: str):
    """
    初始化模型響應
    """
    system_prompt = (
        "你是一個幫助檢查問答品質的 AI 評估員。\n"
        "你的任務是根據使用者的問題與機器人的回答，判斷該回答是否有涵蓋問題的重點。\n"
        "即使回答中未完整說明，但只要有引導到解決方法、提供正確方向或涵蓋關鍵資訊，都算作【有回答到問題】。\n"
        "請只回傳 'Yes' 或 'No'，不要包含其他文字。"
    )

    user_prompt = f"""使用者問題：{question}
        機器人回答：{answer}
        請問這個回答是否有實質回應到問題？"""

    client = init_client()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # ← ✅ 這裡改成你有 quota 的模型
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )
    return response

