class ChatBot:
    def __init__(self, client):
        self.client = client

    # Web search tool integration
    def web_search(self, query):
        response = self.client.responses.create(
            model="gpt-5",
            tools=[{"type": "web_search"}],
            input=query,
            include=["web_search_call.action.sources"],
        )
        # Return the full response object; caller can access response.output_text
        return response

    # Additional tools can be integrated here