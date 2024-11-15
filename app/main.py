# TODO:
# - chat_endpoint:
#   - Input: prompt, user wallet?, [...]
#   - Output: Recomendaction, Action?

import os
from flask import Flask, request, jsonify
from agents import DeFiAgent

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        wallet = data.get('wallet')

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        if not wallet:
            return jsonify({'error': 'Wallet is required'}), 400

        openai_api_key = os.environ.get('OPENAI_API_KEY')
        agent = DeFiAgent(openai_api_key)
        user_input = prompt
        result = agent.process_request(user_input, wallet)
        print("Classification:", result['classification'])
        print("Result:", result['result'])
        print("Summary:", result['summary'])

        response = {
            'summary': result['summary'],
            'action': result['result']
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_address_positions', methods=['POST'])
def get_address_positions():
    data = request.get_json()
    wallet = data.get('wallet')

    pass
    # return jsonify(positions)

if __name__ == '__main__':
    app.run(debug=True)
