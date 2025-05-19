import os
from dotenv import load_dotenv
from openai import AzureOpenAI

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