class AssistantRunner:
    def __init__(self, client, assistant):
        self.client = client
        self.assistant = assistant
        self.thread = None

    def create_thread(self):
        """
        創建新的對話線程
        """
        self.thread = self.client.beta.threads.create()
        return self.thread

    def add_message(self, message):
        """
        添加用戶消息到對話線程
        """
        if not self.thread:
            self.create_thread()
        
        return self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )

    def run_assistant(self):
        """
        運行 assistant 處理當前對話
        """
        if not self.thread:
            raise ValueError("No thread created. Please add a message first.")

        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )
        return run

    def get_messages(self):
        """
        獲取對話歷史
        """
        if not self.thread:
            return []
            
        return self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        ) 