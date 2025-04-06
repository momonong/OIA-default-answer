import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from app.tool_registry import get_tool_definition, get_tool_resources


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
        instructions="",
        tools=get_tool_definition(),
        tool_resources=get_tool_resources(),
        temperature=1,
        top_p=1,
    )

    return assistant
