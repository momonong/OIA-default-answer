from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def init_client():
    """
    初始化 Azure client
    """
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version="2024-12-01-preview",
    )
    return client


def get_embedding_response(texts):
    """
    初始化嵌入響應
    """
    client = init_client()
    response = client.embeddings.create(model="text-embedding-3-large", input=texts)
    return response


if __name__ == "__main__":
    # 測試嵌入
    texts = ["這是一個測試", "這是另一個測試"]
    response = get_embedding_response(texts)
    for text, embedding in zip(texts, response.data):
        print(f"文本：{text}，嵌入：{embedding.embedding}")
