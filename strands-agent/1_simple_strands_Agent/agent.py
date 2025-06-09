import requests
import json
import os
from strands import Agent
from strands_tools import calculator
from strands import tool
from strands.types.tools import ToolResult, ToolUse
from typing import Any
from dotenv import load_dotenv

# Load .env file
load_dotenv()

@tool(name="get_weather_info_for_given_zipcode", description="Retrieves weather forecast for a specified zipcode")
def get_weather_info_for_given_zipcode(zipcode: str) -> ToolResult:
    """
    Get the weather forecast for a given zipcode.
    """
    print(f"Fetching weather information for zipcode: {zipcode}")
    try:
        # Use the provided zipcode parameter
        url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode}&appid={os.getenv('OPENWEATHER_API_KEY')}"
        print(f"Requesting URL: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad status codes
        
        data = response.json()
        weather_info = f"Weather in {data['name']}: {data['weather'][0]['description']}, Temperature: {round(data['main']['temp'] - 273.15, 1)}°C"
        
        return {
            "toolUseId": 123,
            "status": "success",
            "content": [{"text": json.dumps(data)}]
        }
    except Exception as e:
        error_msg = f"Error retrieving weather data: {str(e)}"
        print(error_msg)
        
        return {
            "toolUseId": 123,
            "status": "error",
            "content": [{"text": f"Unable to retrieve weather data for zipcode {zipcode}. Error: {str(e)}"}]
        }


# 1. Tool Specification
TOOL_SPEC = {
    "name": "gather_pizza_order_info",
    "description": "Gather pizza order information from the user..",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "baseType": {
                    "type": "string",
                    "description": "Ask user to choose base type as thick or thin or regular or cheese crust",
                    "default": "thick"
                },
                "size": {
                    "type": "string",
                    "description": "Ask user to provide size of pizza as small, medium or large",   
                    "default": "medium"
                },
                "toppings": {
                    "type": "array",
                    "description": "Ask user to choose toppings from the list: ['pepperoni', 'mushrooms', 'onions', 'sausage', 'bacon', 'extra cheese', 'black olives', 'green peppers', 'pineapple', 'spinach']",
                    "items": {
                        "type": "string"
                    },
                    "default": ["pepperoni", "mushrooms"]
                }
            },
            "required": ["baseType", "size", "toppings"]
        }
    }
}

@tool(name=TOOL_SPEC["name"], description=TOOL_SPEC["description"], inputSchema=TOOL_SPEC["inputSchema"])
def gather_pizza_order_info(tool: ToolUse) -> ToolResult:
    """
    Gather pizza order information from the user.
    Args:
        baseType (str): Type of pizza base.
        size (str): Size of the pizza.
        toppings (list): List of toppings chosen by the user.
    Returns:
        dict: Pizza order information.
    """
    # Extract tool parameters
    tool_use_id = tool["toolUseId"]
    tool_input = tool["input"]
    
    # get the parameters from the tool input
    base_type = tool_input.get("baseType", "")
    size = tool_input.get("size", "")
    toppings = tool_input.get("toppings", [])
    
    return {
        "toolUseId": tool_use_id,
        "status": "success",
        "content": [{
            "text": f"Pizza order received: Base Type: {base_type}, Size: {size}, Toppings: {', '.join(toppings)}"
        }]
    }

# Create an agent with default settings
agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    system_prompt=(
        "You are a helpful assistant that can answer questions and perform tasks using tools. "
        "You can use tools to gather information, perform calculations, and provide weather forecasts for given zipcode. "
        "You can use tools to take pizza orders from users. You must first get the pizza order information from the user. "
        "You can use the tool to gather weather information for a given zipcode. "
        "Do not apologize in your responses. "
        "Use the tools provided to assist users with their requests."
    ),
    tools=[calculator, get_weather_info_for_given_zipcode, gather_pizza_order_info]
)

# Ask the agent a question

print('Welcome to the Strands Agent! You can ask questions or request tasks. Type "exit" to quit.')
while True:
    user_input = input("\n> ")
    if user_input.lower() == "exit":
        print("\nGoodbye! 👋")
        break
    response = agent(user_input)
    print("\n===Agent Response:==")
    print(str(response))
    print("\n===END Agent Response:==")