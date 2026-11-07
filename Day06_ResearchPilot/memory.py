from langchain_core.messages import HumanMessage, AIMessage

class ConversationMemory:
    def __init__(self):
        self.history = []

    def add_user_message(self, message: str):
        self.history.append(
            HumanMessage(content=message)
        )

    def add_ai_message(self, message: str):
        self.history.append(
            AIMessage(content=message)
        )

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []
