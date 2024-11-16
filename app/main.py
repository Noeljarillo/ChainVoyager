# TODO:
# - chat_endpoint:
#   - Input: prompt, user wallet?, [...]
#   - Output: Recomendaction, Action?
# - get_address_positions:
#   - Input: wallet
#   - Output: positions

import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from agents import DeFiAgent
from tools.one_inch_utils import get_chart

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/chat', methods=['POST'])
@cross_origin()
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
        agent = DeFiAgent(openai_api_key, '../db/pools_data.db')
        result = agent.process_request(prompt, wallet)
        response = {
            'classification': result['classification'],
            'summary': result['summary'],
            'result': result['result'],
            'parameters': result['parameters'],
            'action': result['action']
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_address_positions', methods=['POST'])
def get_address_positions():
    data = request.get_json()
    wallet = data.get('wallet')
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    agent = DeFiAgent(openai_api_key, '../db/pools_data.db')
    positions = agent.get_positions(wallet)
    return jsonify(positions)

@app.route('/get_chart_data', methods=['POST'])
def get_chart_data():
    try:
        data = request.get_json()
        wallet = data.get('wallet')
        chain_id = data.get('chain_id')
        timerange = data.get('timerange')

        chart = get_chart(wallet, chain_id, timerange)
        return jsonify(chart)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
