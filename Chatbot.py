class ChatBot:
    def __init__(self, client):
        self.client = client

    # Web search tool integration. Look into adding fields for filtering domains and formatting results based on user needs.
    def web_search(self, query):
        response = self.client.responses.create(
            model="gpt-5",
            tools=[{"type": "web_search"}],
            input=query,
            include=["web_search_call.action.sources"],
        )
        # Return the full response object; caller can access response.output_text
        return response
    
    # File search tool. Connect to MCP database. Requires API key with file search access. Maybe use vector DB? 
    def file_search(self, query):
        response = self.client.responses.create(
            model="gpt-5-mini",
            tools=[{"type": "file_search"}],
            input=query,
            include=["file_search_call.action.sources"],
        )
        return response
    
    