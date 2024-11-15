import os
from dotenv import load_dotenv

load_dotenv()

# Classifier Prompt Template
def get_classifier_prompt(user_input):
    return f"""
You are a classifier for a DeFi application. Categorize the following user input into one of the five categories:

IF THE QUESTION IS NOT ABOUT CRYPTOCURRENCY, RETURN 5. You cannot invest in any other assets.

1. Swap two tokens (or buy/sell)
2. Optimize a portfolio (optimize address tokens and positions)
3. Create new position (open a position in an LP)
4. Explain current positions or assets in the wallet
5. Other

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

# Explain positions prompt template
def get_explain_positions_prompt(positions):
    return f"""
You are an assistant that explains DeFi positions and token holdings in a clear and understandable way.

Here are the positions and holdings to explain:
{positions}

Please provide a clear explanation of:
1. Token holdings (ETH, USDC, etc) and their current values
2. Active liquidity providing positions, including:
   - Token pairs
   - Amount of tokens provided
   - Current APY/rewards
3. Active lending positions, including:
   - Assets being lent
   - Interest rates
   - Collateral if applicable
4. Any other relevant DeFi positions or investments

Explain in simple terms that a non-technical user can understand. Include approximate USD values where possible.
"""
