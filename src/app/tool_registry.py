def get_tool_definition():
    """
    取得工具的定義
    """
    return [
        {"type": "file_search"},
        {"type": "code_interpreter"},
        {
            "type": "function",
            "function": {
                "name": "get_preferred_answer",
                "description": "從 Google Sheet 的常見問答中找出最接近的問題",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "使用者提出的問題",
                        }
                    },
                    "required": ["query"],
                },
            },
        },
    ]


def get_tool_resources():
    """
    取得工具的資源
    """
    return {
        "file_search": {"vector_store_ids": []},
        "code_interpreter": {"file_ids": []},
    }
