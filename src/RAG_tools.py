from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

class MongoDBRAG:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize Azure OpenAI clients
        self.embedding_client = AzureOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            api_version=os.getenv("EMBEDDING_VERSION"),
            azure_endpoint=os.getenv("AZURE_EMBE_ENDPOINT")
        )

        self.chat_client = AzureOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            api_version=os.getenv("CHAT_VERSION"),
            azure_endpoint=os.getenv("AZURE_LLM_ENDPOINT")
        )
        
        # MongoDB connection parameters
        self.mongo_uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("DB_NAME")
    
    def search_similar_documents(self, query_embedding, limit=2, identity="international") -> list:
        """
        Perform vector search in MongoDB collection to find similar documents.

        Args:
        query_embedding (list): Embedding vector of the query text
        limit (int): Maximum number of results to return

        Returns:
        list: List of matching documents
        """
        client = MongoClient(self.mongo_uri, server_api=ServerApi('1'))
        db = client[self.db_name]
        collection = db[f'{identity}_docs']
        
        # Define vector search stage
        vector_search_stage = {
            "$vectorSearch": {
                "index": "vector_index",  # 修改 index name
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 100,
                "limit": limit
            }
        }

        # Execute aggregation pipeline
        try:
            pipeline = [vector_search_stage]
            results = list(collection.aggregate(pipeline))
            
            # Get query execution statistics in a safer way
            try:
                explain_query = db.command(
                    'explain',
                    {
                        'aggregate': collection.name,
                        'pipeline': pipeline,
                        'cursor': {}
                    },
                    verbosity='executionStats'
                )
                print("Explain query results:", explain_query)  # Debug output
                
                # Try to extract execution time if available
                if 'executionStats' in explain_query:
                    execution_time = explain_query['executionStats'].get('executionTimeMillis', 0)
                    print(f"Query execution time: {execution_time} milliseconds")
                
            except Exception as stats_error:
                print(f"Note: Could not get execution statistics: {stats_error}")
            
            return results
        
        except Exception as e:
            print(f"Error during vector search: {str(e)}")
            print("Error details:", e.__class__.__name__)  # Print error type
            return []
        finally:
            client.close()

    def get_embedding(self, text) -> list:
        """
        Get embedding vector for the input text
        
        Args:
        text (str): Input text to embed
        
        Returns:
        list: Embedding vector
        """
        response = self.embedding_client.embeddings.create(
            input=text,
            model="text-embedding-3-large"
        )
        return response.data[0].embedding

    def get_chat_response(self, query, results, language) -> str:
        """
        Generate a chat response based on the query and search results
        
        Args:
        query (str): User query
        results: Search results to include in the prompt
        
        Returns:
        str: Generated response from the model
        """
        response = self.chat_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": '''You are a chatbot dedicated to answering user questions.
                Use the following pieces of context to answer the question at the end. If you don't know the answer, 
                just say that it is recommended to ask the International Office staff, don't try to make up an answer.'''},
                {"role": "user", "content": f"Query: {query}\nResults: {results}"},
                {"role": "system", "content": f"Do not use any formatting in your answer.\nAnswer in {language}:"}
            ]
        )
        return response.choices[0].message.content
    
    def process_query(self, query, limit=2, identity="international", language="English"):
        """
        Process a user query end-to-end
        
        Args:
        query (str): User query
        limit (int): Maximum number of documents to retrieve
        
        Returns:
        dict: Results containing search results and chat response
        """
        query_embedding = self.get_embedding(query)  
        results = self.search_similar_documents(query_embedding, limit, identity)
        
        print("查詢:", query)
        print("\n搜尋結果:")
        if results:
            for i, doc in enumerate(results, 1):
                print(f"\n文件 {i}:")
                print(f"檔案名稱: {doc.get('filename', 'N/A')}")
                print(f"內容: {doc.get('content', 'N/A')}")
                print("-" * 50)
        else:
            print("未找到相關文件")
            
        print(f"找到 {len(results)} 個文件")
        
        if results:
            response = self.get_chat_response(query, results[0], language)
            print(response)
            return {"results": results, "response": response}
        else:
            return {"results": [], "response": "未找到相關資訊"}




def main():
    rag = MongoDBRAG()
    query = "選課網站是甚麼?"
    identity = "international"
    rag.process_query(query, 2, identity, language="Traditional Chinese")


if __name__ == "__main__":
    main()