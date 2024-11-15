import os
import openai
from prompts import get_classifier_prompt, get_summarizer_prompt
from dotenv import load_dotenv

load_dotenv()

class DeFiAgent:
    def __init__(self, openai_api_key):
        self.client = openai.OpenAI(api_key=openai_api_key)
        self.model_name = 'gpt-4o'

    def classify_user_input(self, user_input):
        prompt = get_classifier_prompt(user_input)
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are an assistant that classifies user inputs into actions."},
                {"role": "user", "content": prompt}
            ]
        )
        classification = response.choices[0].message.content.strip()
        return classification

    def summarize_actions(self, classification, user_input):
        prompt = get_summarizer_prompt(classification, user_input)
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes actions for the user."},
                {"role": "user", "content": prompt}
            ]
        )
        summary = response.choices[0].message.content.strip()
        return summary

    def process_request(self, user_input, user_wallet):
        classification = self.classify_user_input(user_input)
        if not classification or classification == '5':
            return {
                'classification': classification,
                'result': None,
                'summary': "I can only assist with the following actions: Swap tokens, Optimize portfolio, Create new position."
            }
        result = self.execute_action(classification, user_input, user_wallet)
        summary = self.summarize_actions(classification, user_input)
        return {
            'classification': classification,
            'result': result,
            'summary': summary
        }

    # Template for functionalities
    def swap_tokens(self, user_input, user_wallet):
        # Implement the logic to swap two tokens
        print("Executing token swap... " + user_wallet)
        return {
            'result': {
                'token_1': 'DAI',
                'token_2': 'USDC',
                'amount_token_1': 100,
                'amount_token_2': 100
            }
        }

    def optimize_portfolio(self, user_input, user_wallet):
        # Implement the logic to optimize the portfolio
        print("Optimizing portfolio... " + user_wallet)
        return {
            'result': {
                'token_1': 'DAI',
                'token_2': 'USDC',
                'amount_token_1': 100,
                'amount_token_2': 100
            }
        }

    def create_new_position(self, user_input, user_wallet):
        # Implement the logic to open a new position in an LP
        print("Creating new liquidity position... " + user_wallet)
        return {
            'result': {
                'token_1': 'DAI',
                'token_2': 'USDC',
                'amount_token_1': 100,
                'amount_token_2': 100
            }
        }

    def handle_other(self, user_input):
        # Inform the user that only the specified options are available
        print("Action not recognized. Please choose a valid option.")

    def execute_action(self, classification, user_input, user_wallet):
        if '1' in classification:
            return self.swap_tokens(user_input, user_wallet)
        elif '2' in classification:
            return self.optimize_portfolio(user_input, user_wallet)
        elif '3' in classification:
            return self.create_new_position(user_input, user_wallet)
        elif '4' in classification:
            return self.explain_positions(user_input, user_wallet)
        else:
            return None

if __name__ == "__main__":
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    agent = DeFiAgent(openai_api_key)
    user_input = "Can you invest some of my tokens in gold?"
    user_wallet = "0x1234567890123456789012345678901234567890"
    result = agent.process_request(user_input, user_wallet)
    print("Classification:", result['classification'])
    print("Result:", result['result'])
    print("Summary:", result['summary'])
