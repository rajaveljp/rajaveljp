import asyncio
import os
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP
from dotenv import load_dotenv
#import logfire
import os

#logfire.configure(token='your-logfire-token')
#logfire.instrument_pydantic_ai()
load_dotenv()
OPENAI_API_KEY = ""
MCP_SERVER_URL = "http://localhost:8000/sse"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
async def chat_with_agent(prompt: str) -> str:
    """
    Send a message to the LLM with access to the MCP tools.
    
    Args:
        prompt: The user's message
        
    Returns:
        String response from the agent
    """
    try:
        # Create the MCP server connection
        server = MCPServerHTTP(url=MCP_SERVER_URL)
        
        # Set up the agent with the MCP server and explicitly pass the API key
        # Different models use different providers, so we need to set up credentials differently
        agent = Agent(
            model="openai:gpt-4o",
            api_key=OPENAI_API_KEY,  # Explicitly pass the API key
            mcp_servers=[server]
        )
        
        # Run the agent with the MCP server context
        async with agent.run_mcp_servers():
            result = await agent.run(prompt)
            
        return result.output
            
    except Exception as e:
        #logger.error(f"Error in chat_with_agent: {str(e)}")
        return f"Error occurred: {str(e)}"

async def main():
    """Main function to demonstrate the client usage"""
    
    print(f"Using API key: {OPENAI_API_KEY[:8]}...{OPENAI_API_KEY[-4:]}")
    
    # Example prompts that should trigger tool usage
    test_prompts = [
        "What is 25 * 16?",
        "What's the current temperature in Tokyo?"
    ]
    
    # Interactive mode
    print("\n=== Calculator and Weather Agent ===")
    print("Type 'exit' to quit the program")
    
    # Process the example prompts first
    for prompt in test_prompts:
        print(f"\n[Example] You: {prompt}")
        response = await chat_with_agent(prompt)
        print(f"Agent: {response}")
    
    # Then enter interactive mode
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Exiting...")
            break
            
        response = await chat_with_agent(user_input)
        print(f"Agent: {response}")

if __name__ == "__main__":
    asyncio.run(main())