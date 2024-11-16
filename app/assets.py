import json
from tools.one_inch_utils import get_protocol_details, get_current_value, get_token_details

EXAMPLE_WALLET = '0x9558c18138401bCD4caE96f8be6C5caF22AD2cbf'

def get_address_positions(wallet_address: str, chain_id: str):
    protocol_details = get_protocol_details(wallet_address, chain_id)
    if isinstance(protocol_details, dict):
        data = protocol_details
    else:
        # If it's a string, ensure it's valid JSON
        protocol_details_json = protocol_details.replace("'", '"')
        data = json.loads(protocol_details_json)
    positions = []
    for item in data.get('result', []):
        protocol_name = item.get('protocol_name', '')
        underlying_tokens = item.get('underlying_tokens', [])
        for token in underlying_tokens:
            position = {
                'protocol_name': protocol_name,
                'underlying_asset': token.get('address', ''),
                'amount_invested_tokens': token.get('amount', 0),
                'amount_invested_usd': token.get('value_usd', 0)
            }
            positions.append(position)
    return positions

def get_address_assets(wallet_address: str, chain_id: str):
    current_value = get_current_value(wallet_address, chain_id)
    return current_value

if __name__ == "__main__":
    print(get_address_assets(EXAMPLE_WALLET, 1))
