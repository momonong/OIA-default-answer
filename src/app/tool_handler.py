import json
from src.functions.preferred_answer import get_preferred_answer


def handle_tool_call(tool_call):
    """
    處理工具呼叫
    """
    if tool_call.function.name == "get_preferred_answer":
        args = json.load(tool_call.function.arguments)
        answer = get_preferred_answer(args["query"])
        return {"tool_call_id": tool_call.id, "output": answer or "查無匹配"}

    return None
