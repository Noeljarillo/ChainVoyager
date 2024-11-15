import unittest
import json
from unittest.mock import patch, MagicMock
from main import app

class TestFlaskAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.headers = {'Content-Type': 'application/json'}
        self.wallet = "0x7B65d2662De442Eb0f79E27b9D870d96D7A6c8bA"

    @patch('main.DeFiAgent')
    def test_chat_endpoint_valid_prompt(self, mock_agent_class):
        # Mock the DeFiAgent instance and its methods
        mock_agent = MagicMock()
        mock_agent.process_request.return_value = {
            'classification': '1',
            'result': {'key': 'value'},
            'summary': 'You requested to swap tokens.'
        }
        mock_agent_class.return_value = mock_agent

        data = {
            'prompt': 'I want to swap 100 DAI for USDC.',
            'wallet': self.wallet
        }
        response = self.app.post('/chat', headers=self.headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('summary', response_data)
        self.assertIn('action', response_data)
        self.assertEqual(response_data['action'], {'key': 'value'})

    @patch('main.DeFiAgent')
    def test_chat_endpoint_missing_prompt(self, mock_agent_class):
        data = {
            'wallet': self.wallet
        }
        response = self.app.post('/chat', headers=self.headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('error', response_data)

    @patch('main.DeFiAgent')
    def test_chat_endpoint_agent_exception(self, mock_agent_class):
        # Mock the DeFiAgent to raise an exception
        mock_agent = MagicMock()
        mock_agent.process_request.side_effect = Exception("Test exception")
        mock_agent_class.return_value = mock_agent

        data = {
            'prompt': 'I want to swap 100 DAI for USDC.',
            'wallet': self.wallet
        }
        response = self.app.post('/chat', headers=self.headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 500)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Test exception')

if __name__ == '__main__':
    unittest.main()