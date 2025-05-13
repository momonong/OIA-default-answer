import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from tool_registry import get_tool_definition, get_tool_resources


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
            You are a helpful assistant that answers student questions using two tools:

            Tools available:
            1. `get_preferred_answer(query: string)`: Retrieves a short, pre-written answer from International Office staff, or returns null if no match is found.
            2. `get_context_from_mongodb(identity: string, query: string)`: Retrieves relevant information from a database based on student identity (e.g., international, chinese, oversea).

            Answering procedure:

            1. First, call `get_preferred_answer(query)` to check for an official answer.
                - If an answer is found:
                    - You **must keep the core content and meaning unchanged**.
                    - You **may slightly rephrase or enhance the fluency** of the response to sound more natural or friendly.
                    - You may also **add brief contextual or transitional phrases**, as long as they don’t modify or dilute the original intent.
                - If no answer is found (null or empty), proceed to step 2.

            2. Call `get_context_from_mongodb(identity, query)` using the user's identity.
                - Use the retrieved context to generate a full, accurate, and student-appropriate answer.
                - Rephrase and summarize as needed, while preserving factual accuracy.

            Additional instructions:
            - Never fabricate or guess any answer.
            - If the student’s identity is missing or unclear, ask the user to clarify before using MongoDB.
            - Always respond in a friendly, clear, and helpful tone.
        """,
        tools=get_tool_definition(),
        tool_resources=get_tool_resources(),
        temperature=1,
        top_p=1,
    )

    return assistant
