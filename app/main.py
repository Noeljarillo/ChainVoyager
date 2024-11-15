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
        wallet = data.get('wallet')  # Optional wallet parameter

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        openai_api_key = os.environ.get('OPENAI_API_KEY')
        agent = DeFiAgent(openai_api_key)
        user_input = prompt
        result = agent.process_request(user_input)
        print("Classification:", result['classification'])
        print("Result:", result['result'])
        print("Summary:", result['summary'])

        response = {
            'recommendation': f'Received prompt: {prompt}',
            'action': None
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)