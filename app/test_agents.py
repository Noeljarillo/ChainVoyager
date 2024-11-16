import unittest
import os
from unittest.mock import patch, MagicMock
from agents import DeFiAgent

class TestDeFiAgent(unittest.TestCase):
    def setUp(self):
        self.agent = DeFiAgent(openai_api_key=os.environ.get('OPENAI_API_KEY'))
        self.user_wallet = "0x7B65d2662De442Eb0f79E27b9D870d96D7A6c8bA"

    @patch('openai.ChatCompletion.create')
    def test_classify_user_input_swap_tokens(self, mock_openai):
        # Mock the response from OpenAI API for classification
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "1"
        mock_openai.return_value = mock_response

        user_input = "I want to swap 100 DAI for USDC."
        classification = self.agent.classify_user_input(user_input)
        self.assertEqual(classification, "1")

        # Test execute_action method
        result = self.agent._execute_action(classification, user_input, self.user_wallet)
        self.assertIn('result', result)

    @patch('openai.ChatCompletion.create')
    def test_summarize_actions(self, mock_openai):
        # Mock the response from OpenAI API for summarization
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "You requested to swap 100 DAI for USDC."
        mock_openai.return_value = mock_response

        classification = "1"
        user_input = "I want to swap 100 DAI for USDC."
        parameters = {"token_in": "DAI", "token_out": "USDC", "amount_in": 100}
        result = {"token_1": "DAI", "amount_1": 100, "token_2": "USDC", "amount_2": 99.99}
        summary = self.agent._summarize_actions(classification, user_input, parameters, result)
        self.assertIsNotNone(summary)

    @patch('openai.ChatCompletion.create')
    def test_process_request_invalid_input(self, mock_openai):
        # Mock the response from OpenAI API for classification
        mock_response_classify = MagicMock()
        mock_response_classify.choices[0].message.content = "5"
        mock_openai.side_effect = [mock_response_classify]

        user_input = "Can you invest in gold?"
        result = self.agent.process_request(user_input, self.user_wallet)
        self.assertEqual(result['classification'], "5")
        self.assertIsNone(result['result'])
        self.assertIn("I can only assist with the following actions", result['summary'])

    @patch('openai.ChatCompletion.create')
    def test_swap_tokens_action(self, mock_openai):
        # Mock classification response
        mock_response_classify = MagicMock()
        mock_response_classify.choices[0].message.content = "1"
        # Mock summarization response
        mock_response_summarize = MagicMock()
        mock_response_summarize.choices[0].message.content = "Action summary."

        mock_openai.side_effect = [mock_response_classify, mock_response_summarize]

        user_input = "Swap 50 ETH for DAI."
        result = self.agent.process_request(user_input, self.user_wallet)
        self.assertEqual(result['classification'], "1")
        self.assertIsNotNone(result['result'])
        self.assertIsNotNone(result['summary'])

    @patch('openai.ChatCompletion.create')
    def test_handle_other_action(self, mock_openai):
        # Mock classification response
        mock_response_classify = MagicMock()
        mock_response_classify.choices[0].message.content = "5"

        mock_openai.return_value = mock_response_classify

        user_input = "Tell me a joke."
        result = self.agent.process_request(user_input, self.user_wallet)
        self.assertEqual(result['classification'], "5")
        self.assertIsNone(result['result'])
        self.assertIn("I can only assist with the following actions", result['summary'])

if __name__ == '__main__':
    unittest.main()
