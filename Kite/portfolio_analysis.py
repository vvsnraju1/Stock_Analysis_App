import logging
import os
import asyncio
from agents import Agent, Runner, MCPServerSse
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

async def analyze_portfolio():
    # Set your OpenAI API key
    if "OPENAI_API_KEY" not in os.environ:
        api_key = input("Enter your OpenAI API key: ")
        os.environ["OPENAI_API_KEY"] = api_key
    
    # Connect to the Zerodha Kite MCP server
    async with MCPServerSse(
        params={
            "url": "https://mcp.kite.trade/sse"
        }
    ) as kite_server:
        # Create a specialized portfolio analysis agent
        portfolio_agent = Agent(
            name="Portfolio Analyzer",
            instructions="""
            You are a specialized portfolio analysis assistant with access to the user's Zerodha account data.
            
            Your primary tasks are to:
            1. Retrieve the user's current portfolio holdings
            2. Analyze sector diversification and risk exposure
            3. Identify underperforming and outperforming investments
            4. Calculate key metrics like P/E ratios, dividend yields, and historical performance
            5. Provide actionable insights for portfolio optimization
            
            Focus solely on portfolio analysis - do not provide general investment advice 
            or recommendations for new investments unless specifically requested.
            
            Base all your analysis on real-time data from the user's Zerodha account.
            """,
            mcp_servers=[kite_server],
            model="gpt-4o-mini",
            model_settings=ModelSettings(store=False)  # This prevents data from being sent to OpenAI dashboard
        )
        
        print("Portfolio Analysis Assistant is ready!")
        
        # Predefined analysis queries
        analysis_queries = [
            "Show me a summary of my current portfolio holdings",
            "Analyze the sector diversification of my portfolio",
            "Identify my top 3 performing and bottom 3 performing stocks",
            "Calculate the average P/E ratio and dividend yield of my portfolio",
            "What's my portfolio's overall exposure to market volatility?"
        ]
        
        # Run each analysis query
        for i, query in enumerate(analysis_queries, 1):
            print(f"\n--- Analysis {i}: {query} ---")
            result = await Runner.run(portfolio_agent, query)
            print(f"\nResults: {result.final_output}")
            
            # Pause between queries to avoid rate limiting
            if i < len(analysis_queries):
                print("\nMoving to next analysis in 3 seconds...")
                await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(analyze_portfolio()) 