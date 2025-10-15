import asyncio
import os
import sys
from pathlib import Path

import logging
logging.basicConfig(level=logging.DEBUG)

# Import from openai-agents library BEFORE adding src to path
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from openai import AsyncOpenAI

# Add src to path for local imports
if __name__ == "__main__":
    src_path = Path(__file__).parent.parent
    sys.path.insert(0, str(src_path))

from tools.vector_search import VectorSearchTool, search_knowledge_base 


set_tracing_disabled(True)

client = AsyncOpenAI(base_url=os.getenv("OPENAI_API_ENDPOINT"))
model = OpenAIChatCompletionsModel(openai_client=client, model="gpt-4.1")

# The agent below should answer questions related to Federal Reserve speeches.
# It is still incomplete:
# - Add specific instructions for the agent to follow when answering questions.
# - Add a function tool that performs vector search, and pass it to the agent
# - Tip: there are different function tool execution modes

async def main():
    @function_tool
    async def vector_search(query: str):
        """
        Perform a vector search using Qdrant with FastEmbed.

        Args:
            query: The user query string.

        Returns:
            A list of relevant document chunks with metadata.
        """
        tool = VectorSearchTool(
            qdrant_url=os.getenv("QDRANT_URL"),
            qdrant_api_key=os.getenv("QDRANT_API_KEY"),
            collection_name="fed_speeches",
            model_name="BAAI/bge-small-en"
        )
        results = tool.search(query)
        return results
              
    agent = Agent(
        name="FedSpeechAgent",
        instructions="Please answer questions related to Federal Reserve speeches using the provided vector search tool.",
        model=model,
        tools=[vector_search],
    )

    result = await Runner.run(agent, "What's the fed overview about monetary policy as of August 2025?")
    return result.final_output

if __name__ == "__main__":
    
    result = asyncio.run(main())
    print(result)