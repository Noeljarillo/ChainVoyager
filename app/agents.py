import os
import openai
import json
from dotenv import load_dotenv
from prompts import get_classifier_prompt, get_summarizer_prompt, \
    get_swap_parameters_prompt, get_explain_positions_prompt, \
    get_optimize_portfolio_parameters_prompt, get_create_new_position_parameters_prompt, \
    get_explore_pools_parameters_prompt, get_explore_pools_prompt

from tools.find_optimal import get_optimal_pools
from pools import PoolsDatabase
from tools.one_inch_utils import get_combined_details
from tools.swap_executor import build_transaction_payload

EXAMPLE_WALLET = '0x9558c18138401bCD4caE96f8be6C5caF22AD2cbf'

load_dotenv()

class DeFiAgent:
    def __init__(self, openai_api_key, db_path):
        self.client = openai.OpenAI(api_key=openai_api_key)
        self.model_name = 'gpt-4o'
        self.db_path = db_path

    def classify_user_input(self, user_input):
        prompt = get_classifier_prompt(user_input)
        classification = self._send_message(prompt, "You are an assistant that classifies user inputs into actions.")
        return classification

    def _summarize_actions(self, classification, user_input, parameters, result):
        prompt = get_summarizer_prompt(classification, user_input, parameters, result)
        summary = self._send_message(prompt, "You are an assistant that summarizes actions for the user.")
        return summary

    def process_request(self, user_input, user_wallet):
        classification = self.classify_user_input(user_input)
        if not classification or classification == '6':
            return {
                'classification': classification,
                'result': None,
                'summary': "I can only assist with the following actions: Swap tokens, Optimize portfolio, Create new position."
            }
        result = self._execute_action(classification, user_input, user_wallet)
        summary = self._summarize_actions(
            classification,
            user_input,
            result['parameters'],
            result['result']
        )
        return {
            'classification': classification,
            'result': result['result'],
            'action': result['action'],
            'summary': summary,
            'parameters': result['parameters']
        }

    def swap_tokens(self, user_input, user_wallet):
        print("Executing token swap... " + user_wallet)

        # Extract parameters from user input
        # Token1, Token2, AmountToken1
        prompt = get_swap_parameters_prompt(user_input)
        parameters = self._send_message(prompt, "You are an assistant that extracts parameters from user inputs.")
        print("Parameters: " + parameters)

        # Generate calldata
        calldata = build_transaction_payload()
        return {
            'result': {
                'token_1': 'DAI',
                'token_2': 'USDC',
                'amount_token_1': 100,
                'amount_token_2': 100
            },
            'action': None,  # TODO: Implement this
            'parameters': parameters
        }

    def optimize_portfolio(self, user_input, user_wallet):
        print("Optimizing portfolio... " + user_wallet)

        # Extract parameters from user input
        prompt = get_optimize_portfolio_parameters_prompt(user_input)
        parameters = self._send_message(prompt, "You are an assistant that extracts parameters from user inputs.")
        print("Parameters: " + parameters)

        # convert parameters to dict
        parameters = json.loads(parameters)
        exposure = parameters.get('exposure')
        stablecoin = parameters.get('stablecoin')
        chain = parameters.get('chain')

        optimal_pools = get_optimal_pools(
            self.db_path,
            exposure=exposure,
            stablecoin=stablecoin,
            chain=chain,
            ilRisk=None,
            project=None,
            symbol=None,
            top_n=3
        )

        # Call proposal generator # TODO: Implement this

        return {
            'result': optimal_pools,
            'action': None,  # TODO: Implement this
            'parameters': parameters
        }

    def create_new_position(self, user_input, user_wallet):
        print("Creating new position... " + user_wallet)

        # Extract parameters from user input
        prompt = get_create_new_position_parameters_prompt(user_input)
        parameters = self._send_message(prompt, "You are an assistant that extracts parameters from user inputs.")
        print("Parameters: " + parameters)

        # TODO: Generate calldata and actions

        summary = self._summarize_actions(
            '3',
            user_input,
            parameters,
            None
        )

        return {
            'result': "",
            'action': None,  # TODO: Implement this
            'parameters': parameters
        }

    def explain_positions(self, user_input, user_wallet):
        print("Explaining positions... " + user_wallet)
        positions = self.get_positions(user_wallet)
        prompt = get_explain_positions_prompt(positions, user_input)
        explanation = self._send_message(prompt, "You are an assistant that explains positions.")

        return {
            'result': explanation,
            'action': None,
            'parameters': None
        }

    def explore_pools(self, user_input, user_wallet):
        print("Exploring pools... " + user_wallet)

        # Get params
        prompt = get_explore_pools_parameters_prompt(user_input)
        parameters = self._send_message(prompt, "You are an assistant that extracts parameters from user inputs.")

        # Get pools
        pools_db = PoolsDatabase(self.db_path)
        pools = pools_db.filter_pools(
            network=parameters.get('network'),
            min_apy=parameters.get('minimum_apy')
        )
        # choose only 3 pools
        pools = pools[:3]
        prompt = get_explore_pools_prompt(pools)
        explanation = self._send_message(prompt, "You are an assistant that explains pools.")
        pools_db.close()
        return {
            'result': explanation,
            'action': pools,
            'parameters': parameters
        }

    def get_positions(self, user_wallet):
        print("Getting positions... " + user_wallet)
        combined_details = get_combined_details(user_wallet, '1', '2023-01-01T00:00:00Z', '2024-11-10T23:59:59Z')
        return combined_details

    def _execute_action(self, classification, user_input, user_wallet):
        if '1' in classification:
            return self.swap_tokens(user_input, user_wallet)
        elif '2' in classification:
            return self.optimize_portfolio(user_input, user_wallet)
        elif '3' in classification:
            return self.create_new_position(user_input, user_wallet)
        elif '4' in classification:
            return self.explain_positions(user_input, user_wallet)
        elif '5' in classification:
            return self.explore_pools(user_input, user_wallet)
        else:
            return None

    def _send_message(self, message, system_message):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content.strip()


if __name__ == "__main__":
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    agent = DeFiAgent(openai_api_key)

    while True:
        user_input = input("Message: \n--> ")
        user_wallet = input("Wallet: \n--> ")
        result = agent.process_request(user_input, user_wallet)
        print("Classification:", result['classification'])
        print("Result:", result['result'])
        print("Summary:", result['summary'])
