import os, json, requests
import pickle
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI 
from langchain_classic.agents import AgentExecutor, Tool 
from langchain_classic.prompts import PromptTemplate 
import azure.cognitiveservices.speech as speech 
from langchain_classic.agents.mrkl.base import ZeroShotAgent

import json
load_dotenv()

def classify_intent(text: str):
    model_api_endpoint = os.getenv("model_endpoint")
    model_api_key = os.getenv("model_api_key")

    response = requests.post(
        url=model_api_endpoint, 
        json={"text": text}, 
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {model_api_key}'
            },)
    data = dict(response.json())
    print(data['prediction'])

    return data['prediction']


def azure_llm():
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("azure_resource_endpoint"),
        api_key=os.getenv('azure_resource_key'),
        api_version='2024-12-01-preview',
        max_tokens=4096,
        temperature=0,
        azure_deployment='gpt-4o-mini'
    )
    return llm

def extract_account_id(text: str):
    import re
    match = re.search(r"\b(\d{3})\b", text)
    return match.group(1) if match else None


def check_balance(account_id: str):
    acct = accounts.get(extract_account_id(account_id), "Does not exist")
    if not acct:
        return {'error': 'Account not found'}
    
def report_card_issues(account_id: str):
    #simulate blocking card

    return {'status': "Blocked", "account_id":account_id, "next_step": "Collect new card in next 48 hrs"}

def unsupported(text: str):

    return "Unsupported intent. Please contact customer support for further assistance."



if __name__ == "__main__":
    accounts = {
        "001":{"name":"Ini", "balance":200000},
        "002":{"name":"Bolu", "balance":420000},
        "003":{"name":"Ebuks", "balance":3000000},
        "004":{"name":"Daniel", "balance":250000}
    }

    llm = azure_llm()

    while True:
        user_input = input('Type your Question here or q to quit: ')

        if user_input.lower() in ['q', 'quit', 'exit']:
            print('exiting...')
            break
        
        # Option 1: Use your custom model for intent classification
        intent_prediction = classify_intent(user_input)
        print(f"Predicted intent: {intent_prediction}")
        
        # Extract account ID using your function
        account_id = extract_account_id(user_input)
        print(f"Extracted account ID: {account_id}")
        
        # Execute appropriate function based on intent
        if intent_prediction == "transactions":
            if account_id:
                response = check_balance(account_id)
            else:
                response = {"error": "Please provide an account ID to check balance"}
        
        elif intent_prediction == "card":
            if account_id:
                response = report_card_issues(account_id)
            else:
                response = {"error": "Please provide an account ID to report card issues"}
        
        else:
            response = unsupported()
        
        print("Response:", response)
        print("-" * 50)