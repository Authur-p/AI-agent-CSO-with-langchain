import os, json, requests
import pickle
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI 
from langchain_classic.agents import AgentExecutor, Tool 
from langchain_classic.prompts import PromptTemplate 
import azure.cognitiveservices.speech as speech 
from langchain_classic.agents.mrkl.base import ZeroShotAgent

from tools import *


load_dotenv()

accounts = {
        'oo1': {'name': 'ini', 'balance': 200000},
        'oo2': {'name': 'bolu', 'balance': 300000},
        'oo3': {'name': 'ebuks', 'balance': 500000},
        'oo4': {'name': 'dan', 'balance': 999999},
    }

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
    
    llm = azure_llm()
    tools = [classify_tool, balance_tool, card_tool, unsupported_tool]

    prompt_agent = """ You are a banking assistant. You MUST follow this steps:
        1. First Always use the IntentClassifier tool to understand the user's intent.
        2. Then based on the classified intent, use the appropriate tool.
        3. If user does not provide an account number, ask them to provide it.

        User query: {input}

        Let's think step by step."""
    
    agent = ZeroShotAgent.from_llm_and_tools(
        llm=llm,
        tools=tools,
        prefix=prompt_agent
    )

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True, # Verbose - to remove too much explanation, go straight to the point
        handle_parsing_errors=True
    )
    result = agent_executor.invoke({"input": "I lost my ATM card. My account is 001, please block"})
    print(result['output'])

