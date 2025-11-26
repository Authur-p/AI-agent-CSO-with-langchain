from langchain_classic.agents import Tool
from main import check_balance, report_card_issues, classify_intent, unsupported

classify_tool = Tool(
    name='IntentClassifier',
    func=classify_intent,
    description='Classifies user intent in a banking conversation.'
)


balance_tool = Tool(
    name="CheckBalance",
    func=check_balance,
    description="Returns account balance for give account_id"
)

card_tool = Tool(
    name="report_card_issue",
    func=report_card_issues,
    description="Block a card and return next step"
)

unsupported_tool = Tool(
    name="unsupported",
    func=unsupported,
    description="It send unsupported, if intent return unsupported"
)