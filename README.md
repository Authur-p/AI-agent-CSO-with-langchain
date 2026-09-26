# 🤖 AI Customer-Service Agent (LangChain + Azure)

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-0078D4?style=flat-square&logo=microsoftazure&logoColor=white)
![Azure Speech](https://img.shields.io/badge/Azure%20AI%20Speech-0078D4?style=flat-square&logo=microsoftazure&logoColor=white)

A **tool-using banking agent** built with **LangChain**. Rather than just generating text, the agent *reasons step by step* and calls the right **tool** for the job — classifying the customer's intent, checking a balance, blocking a lost card, or routing to human support — using **Azure OpenAI (GPT-4o-mini)** as the reasoning engine.

> This is the agentic sibling of the RAG assistants: instead of retrieving documents, it **takes actions** through a defined toolset, orchestrated by a LangChain agent.

---

## ✨ What it does

The agent follows an enforced policy on every request:

1. **Always classify intent first** via the `IntentClassifier` tool.
2. **Act on the intent** with the matching tool.
3. **Ask for an account number** if the user hasn't provided one.

### 🧰 Tools available to the agent

| Tool | Action |
| :-- | :-- |
| `IntentClassifier` | Calls a **deployed intent-classification model** (REST endpoint, bearer-token auth) to label the request |
| `CheckBalance` | Looks up an account balance (account id parsed from the message) |
| `ReportCardIssue` | Blocks a lost/stolen card and returns next steps (collect replacement within 48 h) |
| `Unsupported` | Graceful fallback that routes anything out of scope to human support |

## 🏗️ Architecture

```
User query
   │
   ▼
LangChain ZeroShotAgent (MRKL)  ◀── reasoning by AzureChatOpenAI (gpt-4o-mini, temp 0)
   │  "think step by step"
   ├─▶ IntentClassifier tool ──▶ deployed model API  (/predict)
   ├─▶ CheckBalance tool
   ├─▶ ReportCardIssue tool
   └─▶ Unsupported tool
   │
   ▼
Action + natural-language response
```

- **Agent:** LangChain `ZeroShotAgent` + `AgentExecutor` with `handle_parsing_errors=True`.
- **Reasoning LLM:** `AzureChatOpenAI` (deployment `gpt-4o-mini`, `temperature=0`).
- **Intent tool:** posts the message to a hosted model endpoint (`model_endpoint`) and reads back the predicted intent — decoupling the classifier from the agent so the model can be retrained/redeployed independently.
- **Voice-ready:** integrates `azure.cognitiveservices.speech` for speech I/O.

**Example**
```python
agent_executor.invoke({"input": "I lost my ATM card. My account is 001, please block"})
# → classifies intent → ReportCardIssue → "Your card on account 001 is blocked; collect a replacement within 48 hours."
```

## 🧰 Tech stack

**Agent / LLM:** LangChain (agents, tools, prompt templates), Azure OpenAI GPT-4o-mini
**Services:** deployed intent-classification REST API, Azure AI Speech
**Core:** Python · requests · python-dotenv

## 🗂️ Repository structure

```
├── main.py          # agent setup, tools wiring, Azure LLM, run loop
├── tools.py         # LangChain Tool definitions
├── manual.py        # manual / non-agent walkthrough of the same actions
├── requirements.txt
└── .env             # Azure OpenAI + intent-model endpoint credentials
```

## ▶️ Getting started

```bash
pip install -r requirements.txt
```

`.env`:
```env
azure_resource_endpoint=https://your-resource.openai.azure.com/
azure_resource_key=your_azure_openai_key
model_endpoint=https://your-intent-model/predict
model_api_key=your_model_api_key
```

```bash
python main.py
```

## 🔗 Related

- **[simple-bank-nlp-model](https://github.com/Authur-p/simple-bank-nlp-model)** — the intent classifier this agent calls.
- **[NLP-hosting-model-CSO-with-azure](https://github.com/Authur-p/NLP-hosting-model-CSO-with-azure)** — hosting that model behind an API.
- **[ai-ml-models](https://github.com/Authur-p/ai-ml-models)** — the full production assistant (text + voice) this experimentation fed into.

## 👤 Author

**Daniel Opeyemi** — MSc Machine Learning &amp; Deep Learning, University of Strathclyde
[Portfolio](https://authur-p.github.io/) · [LinkedIn](https://www.linkedin.com/in/daniel-opeyemi-i/) · danielopeyemi840@gmail.com
