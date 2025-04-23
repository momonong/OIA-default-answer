import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from src.app.tool_registry import get_tool_definition, get_tool_resources


def init_client():
    """
    初始化 Azure client
    """
    load_dotenv()

    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-05-01-preview",
    )

    return client


def init_assistant(client):
    """
    初始化 Assistant
    """
    assistant = client.beta.assistants.create(
        model="gpt-4o",
        instructions="""
        You are a helpful assistant with access to the following tools:


        1. `get_preferred_answer(query: string)`: Find the most relevant FAQ-style answer from a Google Sheet.
        2. `get_context_from_mongodb(identity: string, query: string)`: Retrieve relevant context from MongoDB based on the student's identity (e.g., international, chinese, oversea).

        When receiving a user question:

        - First, try using `get_preferred_answer` to see if a similar answer exists.
        -  you must use `get_context_from_mongodb` with the student's identity to retrieve a more detailed answer.

        Stick to this priority order and avoid guessing when information is unclear.

        """,
        tools=get_tool_definition(),
        tool_resources=get_tool_resources(),
        temperature=1,
        top_p=1,
    )

    return assistant
