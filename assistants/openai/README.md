# OpenAI GPT Assistant

This is a Flask-based assistant service that integrates with OpenAI's GPT-4o model to provide customer service chatbot functionality.

## Features

- **GPT-4o Integration**: Uses OpenAI's latest GPT-4o model for intelligent conversations
- **Function Calling**: Supports tool/function calling for extended capabilities
- **Web Search**: Can search the web for product information and prices
- **Customer Information**: Can retrieve customer order information
- **Multi-language Support**: Responds in the same language as the user

## Environment Variables

Required environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: The OpenAI model to use (default: gpt-4o)

## Tools Available

1. **send_text_to_user**: Send a message directly to the user
2. **get_customer_info**: Retrieve customer information by email
3. **web_search**: Search the web for product information and prices

## API Endpoint

- `POST /chat`: Main chat endpoint
  - Request body: `{"sender": "user_id", "text": "user message"}`
  - Response: `[{"recipient_id": "user_id", "text": "bot response"}]`

## Usage

The service runs on port 8088 and provides a REST API for chat interactions. It's designed to work as part of the FreeTalkBot ecosystem.
