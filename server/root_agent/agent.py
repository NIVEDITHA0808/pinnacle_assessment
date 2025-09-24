from google.adk.agents import Agent
from google.genai.types import GenerateContentConfig
from server.rag import search_retrieval_data
from server.prompt import SYSTEM_PROMPT

genai_config = GenerateContentConfig(
    temperature=0.5
)

def context_callback(context, user_input):
    """Callback to modify the agent's context before each interaction."""
    # Here you can modify the context based on user_input or other factors
    # For example, you might want to add retrieval data or other relevant information
    retrieval_data = search_retrieval_data(user_input)
    context += "\n\n" + retrieval_data
    return context

root_agent = Agent(
   name="agent",
   model="gemini-live-2.5-flash-preview-native-audio",
   description="A helpful AI assistant.",
   instruction=SYSTEM_PROMPT,
    before_agent_callback=context_callback,
    generate_content_config=genai_config
)