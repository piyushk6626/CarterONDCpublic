"""
Inventory Creation Conversation Handler Module

This module provides functions for handling conversations related to inventory creation.
It includes utilities for extracting information from user responses, asking questions,
and processing answers in a structured way.
"""

from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
# Fix imports to use the correct package path
from cart_ondc.inventory_creation.whatsappopration import send_message, recive_message
import cart_ondc.inventory_creation.ICsystem_prompts as ICsystem_prompts

# Load environment variables
load_dotenv()

def extract_value(client, conversation, response_format_class, prompt):
    """
    Extracts structured information from a chat conversation using the specified model and response format.

    Args:
        client: The OpenAI client object for making API calls.
        conversation (list): A list of dictionaries representing the chat messages (excluding the system message).
        response_format_class: The Pydantic class to use for parsing the API response.
        prompt (str): The system prompt to guide the model's behavior.

    Returns:
        response_format_class: The structured result parsed by the provided class, or None if extraction fails.
    """
    # Prepend the default system message
    try:
        full_conversation = [
            {"role": "system", "content": prompt}
        ] + conversation

        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=full_conversation,
            response_format=response_format_class,
        )
        
        return completion.choices[0].message.parsed
    except Exception as e:
        print(f"Error in extract_value: {e}")
        return None



def explain_question2(client, conversation):
    """
    Explains the question to the user based on their response.

    Args:
        client: The OpenAI client object for making API calls.
        conversation (list): A list of dictionaries representing the chat messages.

    Returns:
        dict: The assistant's explanation message, or None if an error occurs.
    """
    try:
        # Extract the assistant's last question and the user's response
        assistant_message = next(
            (msg for msg in reversed(conversation) if msg["role"] == "assistant"),
            None
        )
        user_message = next(
            (msg for msg in reversed(conversation) if msg["role"] == "user"),
            None
        )

        if not assistant_message or not user_message:
            raise ValueError("Incomplete conversation: Missing assistant or user message.")

        # Define the system prompt for explanation
        explanation_prompt = [
            {"role": "system", "content": "You are a helpful Assistant. Identify and explain if the user has responded to the question incorrectly.if he has explain the question dont try to provied answer you can give expample if you want but no answer"},
            assistant_message,
            user_message
        ]

        # API call for explanation
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=explanation_prompt
        )
        return completion.choices[0].message.content

    except Exception as e:
        print(f"Error in explain_question: {e}")
        return None

def explain_question(client, conversation, question):
    """
    Explains the question to the user based on their response.

    Args:
        client: The OpenAI client object for making API calls.
        conversation (list): A list of dictionaries representing the chat messages.
        question (str): The original question that needs explanation.

    Returns:
        str: A message explaining the question to the user, or None if an error occurs.
    """
    try:
        # Extract the assistant's last question and the user's response
        assistant_message = next(
            (msg for msg in reversed(conversation) if msg["role"] == "assistant"),
            None
        )
        user_message = next(
            (msg for msg in reversed(conversation) if msg["role"] == "user"),
            None
        )

        if not assistant_message or not user_message:
            raise ValueError("Incomplete conversation: Missing assistant or user message.")

        # Define the system prompt for explanation
        explanation_prompt = [
            {"role": "system", "content": "You are a helpful Assistant. Identify and explain if the user has responded to the question incorrectly.if he has explain the question dont try to provied answer you can give expample if you want but no answer"},
            assistant_message,
            user_message
        ]

        # Generate explanation
        finalquestion="No you did not respond to it correctly the question was " + question
        return finalquestion
    except Exception as e:
        print(f"Error in explain_question: {e}")
        return None



def ask_question2(client, question, response_format_class, prompt, conversation=None, max_attempts=3, attempt=0):
    """
    Asks a question to the user and processes their response recursively, explaining as needed.

    Args:
        client: The OpenAI client object for making API calls.
        question (str): The question to ask the user.
        response_format_class: The class to use for parsing the API response.
        prompt (str): The system prompt to guide the model.
        conversation (list, optional): Existing conversation history. Defaults to an empty list.
        max_attempts (int): Maximum number of attempts to avoid infinite recursion.
        attempt (int): The current attempt count.

    Returns:
        response_format_class: The structured result, or None if all attempts fail.
    """
    if conversation is None:
        conversation = []

    if attempt >= max_attempts:
        print("Maximum attempts exceeded. Stopping the process.")
        return None

    # Send the question to the user
    send_message(question)
    user_response = recive_message()

    # Add the user's response to the conversation
    full_conversation = conversation + [
        {"role": "assistant", "content": question},
        {"role": "user", "content": user_response}
    ] 
    print()
    print("full_conversation")
    print(full_conversation)
    print()

    # Try to extract the value from the response
    structured_response = extract_value(client, full_conversation, response_format_class, prompt)
    if structured_response and getattr(structured_response, "has_answer", False):
        return structured_response

    # If no valid answer, explain the question and retry
    explanation = explain_question(client, full_conversation)
    if explanation:
        print(f"Explanation provided: {explanation}")
        return ask_question(client, explanation, response_format_class, prompt, full_conversation, max_attempts, attempt + 1)
    
    return None
import time
def ask_question(client, question, response_format_class, prompt, bool_attribute, conversation=None, max_attempts=3):
    """
    Asks a question to the user and processes their response, with multiple retry attempts.

    Args:
        client: The OpenAI client object for making API calls.
        question (str): The question to ask the user.
        response_format_class: The Pydantic class to use for parsing the response.
        prompt (str): The system prompt to guide the model.
        bool_attribute (str): The boolean attribute in the response class that indicates a valid answer.
        conversation (list, optional): Existing conversation history. Defaults to None.
        max_attempts (int): Maximum number of attempts to get a valid answer.

    Returns:
        response_format_class: The structured result, or None if all attempts fail.
    """
    conversation = conversation or []
    for attempt in range(max_attempts):
        send_message(question)
        time.sleep(10)  # Wait for user response
        user_response = recive_message()

        conversation.extend([
            {"role": "assistant", "content": question},
            {"role": "user", "content": user_response}
        ])
        print()
        print("full_conversation")
        print(conversation)
        print()
   
        structured_response = extract_value(client, conversation, response_format_class, prompt)
        print(structured_response)
        if structured_response and getattr(structured_response, bool_attribute, False):
            return structured_response

        explanation = explain_question(client, conversation, question)
        if explanation:
            question = explanation
        else:
            break

    print("Maximum attempts exceeded. Exiting.")
    return None
    

# Example usage:
if __name__ == "__main__":
    from pydantic import BaseModel
    from openai import OpenAI
    class Price_Extraction(BaseModel):
        has_price: bool
        price: int

    # Mock client object (replace with actual client initialization)
    load_dotenv()
    api_key=os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)
    # Initialize your OpenAI client here

    
    
    answer=ask_question(client, "what is the price of the product ?", Price_Extraction, ICsystem_prompts.Price)
    # print(answer)