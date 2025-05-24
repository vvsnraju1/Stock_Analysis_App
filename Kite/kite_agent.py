import logging
import os
import asyncio
from agents import Agent, Runner
from agents.mcp import MCPServerSse
from agents import set_tracing_disabled
from agents.model_settings import ModelSettings

# Set environment variables to disable tracing and logging
os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "1"
os.environ["OPENAI_AGENTS_DONT_LOG_MODEL_DATA"] = "1"
os.environ["OPENAI_AGENTS_DONT_LOG_TOOL_DATA"] = "1"

# Disable specific agent logging at the source
logging.getLogger("openai.agents").setLevel(logging.ERROR)
logging.getLogger("openai.agents.tracing").setLevel(logging.ERROR)
logging.getLogger("openai").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

from dotenv import load_dotenv

load_dotenv()

async def main():
    # Set your OpenAI API key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Connect to the Zerodha Kite MCP server
    async with MCPServerSse(
        params={
            "url": "https://mcp.kite.trade/sse"
        }
    ) as kite_server:
        # Create an agent with access to the Kite MCP server
        agent = Agent(
            name="Zerodha Investment Assistant",
            instructions="""
            You are a helpful financial assistant with access to the user's Zerodha trading account.
            You can help with:
            1. Checking portfolio and holdings
            2. Getting real-time market data
            3. Analyzing investment positions
            4. Researching stocks
            
            Important: You must first login to the Zerodha account using the mcp_kite_login tool
            before accessing any account data. Whenever you encounter a "session not found" error,
            use the login tool first to authenticate, then try the original request again.
            
            Be concise and accurate in your responses. Always provide relevant information
            based on the real-time data from the user's Zerodha account.
            """,
            mcp_servers=[kite_server],
            model="gpt-4o-mini",
            model_settings=ModelSettings(store=False)  # This prevents data from being sent to OpenAI dashboard
        )
        
        print("Zerodha Investment Assistant is ready!")
        print("Authenticating with Zerodha Kite...")
        
        # First perform login to establish session
        login_result = await Runner.run(agent, "Login to my Zerodha account first")
        print(f"\nLogin status: {login_result.final_output}")
        
        print("\nType 'exit' to quit")
        
        # Simple chat loop
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == 'exit':
                break
                
            try:    
                result = await Runner.run(agent, user_input)
                print(f"\nAssistant: {result.final_output}")
            except Exception as e:
                if "session not found" in str(e):
                    print("\nSession expired. Re-authenticating...")
                    try:
                        # Re-login if session expired
                        login_result = await Runner.run(agent, "Login to my Zerodha account")
                        print(f"\nLogin status: {login_result.final_output}")
                        
                        # Retry the original query
                        result = await Runner.run(agent, user_input)
                        print(f"\nAssistant: {result.final_output}")
                    except Exception as login_error:
                        print(f"\nAuthentication failed: {login_error}")
                else:
                    print(f"\nError: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 