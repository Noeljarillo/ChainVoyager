import os
from dotenv import load_dotenv

load_dotenv()

# Classifier Prompt Template
def get_classifier_prompt(user_input):
    return f"""
You are a classifier for a DeFi application. Categorize the following user input into one of the four categories:

IF THE QUESTION IS NOT ABOUT CRYPTOCURRENCY, RETURN 4. You cannot invest in any other assets.

1. Swap two tokens (or buy/sell)
2. Optimize a portfolio (optimize address tokens and positions)
3. Create new position (open a position in an LP)
4. Other (Return that the only options are the ones from before)

User Input: {user_input}

Only output the category number.
"""

# Summarizer Prompt Template
def get_summarizer_prompt(classification, user_input):
    return f"""
You are an assistant that summarizes actions to take based on the classification and user input.

Classification: {classification}
User Input: {user_input}

Provide a concise summary of the actions that need to be taken. Remember that the user will need to sign the transactions.
"""
