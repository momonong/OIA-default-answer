from src.functions.preferred_answer import get_preferred_answer


def handle_tool_call(tool_call):
    """
    處理工具呼叫
    """
    if tool_call.function.name == "get_preferred_answer":
        args = tool_call.function.arguments
        print(f"Tool call: {tool_call.id}")
        print(f"Function name: {tool_call.function.name}")
        print(f"Function arguments: {args}")
        answer = get_preferred_answer(args[0])
        print(f"Answer: {answer}")
        return {"tool_call_id": tool_call.id, "output": answer or "查無匹配"}

    return None
