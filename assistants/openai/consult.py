import os
from openai import OpenAI
from datetime import date
from tools import web_search, customer_info
import logger as log
import json

if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

if os.getenv("OPENAI_MODEL") is None:
    raise ValueError("Please set the OPENAI_MODEL environment variable")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
MODEL_NAME = os.getenv("OPENAI_MODEL")
MAX_TOKENS = 1000


def openai_chat(system_prompt, messages):
    logger = log.get_logger()
    logger.info("GPT is chatting with the user")

    # Convert tools to OpenAI function format
    tools = []
    
    # Add customer info tools
    customer_tools = customer_info.get_tools()
    for tool in customer_tools:
        openai_tool = {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["input_schema"]
            }
        }
        tools.append(openai_tool)
    
    # Add web search tools
    web_tools = web_search.get_tools()
    for tool in web_tools:
        openai_tool = {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["input_schema"]
            }
        }
        tools.append(openai_tool)

    # Prepare messages for OpenAI format
    openai_messages = []
    if system_prompt:
        openai_messages.append({"role": "system", "content": system_prompt})
    
    openai_messages.extend(messages)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=openai_messages,
        max_tokens=MAX_TOKENS,
        tools=tools,
        tool_choice="auto"
    )

    # Handle tool calls
    message = response.choices[0].message
    if message.tool_calls:
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            logger.info(f"=======GPT Wants To Call The {tool_name} Tool=======")
            
            if tool_name == "send_text_to_user":
                result = customer_info.send_text_to_user(tool_args["text"])
            elif tool_name == "get_customer_info":
                result = customer_info.get_customer_info(tool_args["email"])
            elif tool_name == "web_search":
                result = web_search.web_search(tool_args["topic"])
            else:
                logger.info("Oh dear, that tool doesn't exist!")
                result = "Tool not found"
            
            return result
    else:
        # No tool call, return the message content
        return message.content


def chat_with_user(user_query):
    print(f"User asked: {user_query}")
    messages = [
        {
            "role": "user",
            "content": user_query,
        }
    ]

    system_prompt = f"""
        You are a customer service assistant of a tech products seller company.
        All your communication with a user is done via text message.
        The user should ask only about order information or consult about tech products, if you detect that the user wants to talk about something not related to this,
        try to turn the conversation around. This is important.
        Use the same language that the user uses. This is important.

        Use web_search tool if user consults prices of tech products. This is important.
        Use the get_customer_info tool if user asks information or status about his order. The user must have provided already their email. This is important. If you do not know a user's email, simply ask a user for their email.
    """

    return system_prompt, messages
