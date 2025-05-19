import json
from run_agent.function.preferred_answer import get_preferred_answer
# from run_agent.function.RAG_tools import MongoDBRAG

def handle_tool_call(tool_call):
    """
    處理工具呼叫
    """
    if tool_call.function.name == "get_preferred_answer":
        args = json.loads(tool_call.function.arguments)  # ✅ 轉成 dict
        print(f"Tool call: {tool_call.id}")
        print(f"Function name: {tool_call.function.name}")
        print(f"Function arguments: {args}")
        print(f"Function arguments type: {type(args)}")
        answer = get_preferred_answer(args["query"])
        print(f"Answer: {answer}")
        return {"tool_call_id": tool_call.id, "output": answer or "查無匹配"}
    
    # elif tool_call.function.name == "get_context_from_mongodb":
    #     mongodb_rag = MongoDBRAG()
    #     args = json.loads(tool_call.function.arguments)  # ✅ 轉成 dict
    #     print(f"Tool call: {tool_call.id}")
    #     print(f"Function name: {tool_call.function.name}")
    #     print(f"Function arguments: {args}")
    #     print(f"Function arguments type: {type(args)}")
    #     answer = mongodb_rag.process_query(args["query"], 1,args["identity"])
    #     print(f"Answer: {answer}")
    #     return {"tool_call_id": tool_call.id, "output": answer}

    return None
