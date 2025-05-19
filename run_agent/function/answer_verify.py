from run_agent.client.gpt41mini_client import get_model_response


def verify_answer_match(question: str, answer: str) -> bool:
    """
    使用 gpt-4.1-mini 模型判斷預設回答是否有回答到使用者問題。
    回傳 True / False。
    """
    response = get_model_response(question, answer)
    reply = response.choices[0].message.content.strip().lower()
    return "yes" in reply