import logging
import os
import asyncio
from agents import Agent, Runner
from agents.mcp import MCPServerSse
from pydantic import BaseModel
from typing import Dict, Any, Optional

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

# Disable tracing programmatically 
set_tracing_disabled(True)

from dotenv import load_dotenv

load_dotenv()

# Define the input schema for portfolio metrics
class PortfolioMetricsInput(BaseModel):
    portfolio_data: Optional[Dict[str, Any]] = None

# Define custom tools for enhanced financial analysis
async def calculate_portfolio_metrics(portfolio_data: Optional[Dict[str, Any]] = None):
    """
    Calculate key portfolio metrics like diversification, sector allocation, and risk metrics.
    This is a placeholder - in a real implementation, this would use actual portfolio data.
    """
    # This function would analyze the portfolio data obtained from Kite MCP
    return {
        "diversification_score": 7.5,
        "sector_allocation": {
            "IT": "32%",
            "Finance": "28%",
            "Manufacturing": "15%",
            "Healthcare": "12%",
            "Others": "13%"
        },
        "risk_metrics": {
            "beta": 1.2,
            "sharpe_ratio": 0.8,
            "volatility": "Medium"
        }
    }

async def main():
    # Set your OpenAI API key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Connect to the Zerodha Kite MCP server
    async with MCPServerSse(
        params={
            "url": "https://mcp.kite.trade/sse"
        }
    ) as kite_server:
        # Create an advanced agent with access to the Kite MCP server
        agent = Agent(
            name="Advanced Zerodha Investment Advisor",
            instructions="""
            You are an advanced financial advisor with access to the user's Zerodha trading account.
            You can help with:
            1. Portfolio analysis and optimization
            2. Real-time market data and technical analysis
            3. Investment strategy recommendations
            4. Risk assessment and management
            5. Stock research with fundamental and technical perspectives
            
            Important: You must first login to the Zerodha account using the mcp_kite_login tool
            before accessing any account data. Whenever you encounter a "session not found" error,
            use the login tool first to authenticate, then try the original request again.
            
            Always base your recommendations on real data from the user's Zerodha account.
            Be precise, data-driven, and actionable in your advice.
            """,
            mcp_servers=[kite_server],
            # Use GPT-4 mini for more advanced analysis capabilities
            model="gpt-4o-mini",
            model_settings=ModelSettings(store=False)  # This prevents data from being sent to OpenAI dashboard
        )
        
        print("Advanced Zerodha Investment Advisor is ready!")
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
                print(f"\nAdvisor: {result.final_output}")
            except Exception as e:
                if "session not found" in str(e):
                    print("\nSession expired. Re-authenticating...")
                    try:
                        # Re-login if session expired
                        login_result = await Runner.run(agent, "Login to my Zerodha account")
                        print(f"\nLogin status: {login_result.final_output}")
                        
                        # Retry the original query
                        result = await Runner.run(agent, user_input)
                        print(f"\nAdvisor: {result.final_output}")
                    except Exception as login_error:
                        print(f"\nAuthentication failed: {login_error}")
                else:
                    print(f"\nError: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 