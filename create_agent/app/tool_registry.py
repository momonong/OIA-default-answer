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
        # {
        #     "type": "function",
        #     "function": {
        #         "name": "get_context_from_mongodb",
        #         "description": "Based the identity of student and query the document from mongodb to get the answer",
        #         "parameters": {
        #             "type": "object",
        #             "properties": {
        #                 "identity": {
        #                     "type": "string",
        #                     "description": "學生的身分，可以填入 international , chinese or oversea",
        #                 },
        #                 "query": {
        #                     "type": "string",
        #                     "description": "使用者提出的問題",
        #                 }
        #             },
        #             "required": ["identity", "query"],
        #         },
        #     },
        # }
    ]


def get_tool_resources():
    """
    取得工具的資源
    """
    return {
        "file_search": {"vector_store_ids": []},
        "code_interpreter": {"file_ids": []},
    }
