import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# API Key and Base URL
BASE_URL = "https://api.1inch.dev/portfolio/portfolio/v4/overview/erc20"
BASE_URL_HISTORY = "https://api.1inch.dev/history/v2.0/history"
BASE_URL_PROTOCOLS = "https://api.1inch.dev/portfolio/portfolio/v4/overview/protocols/details"
API_KEY = os.environ.get("1INCH_API_KEY")
EXAMPLE_WALLET = '0x9558c18138401bCD4caE96f8be6C5caF22AD2cbf'

# Headers for authorization
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def get_protocol_details(wallet_address: str, chain_id: str, include_closed: bool = True, closed_threshold: int = 10, use_cache: bool = False):
    """
    Fetch protocol details including ROI, APR, unclaimed fees, and other metrics.
    """
    params = {
        'addresses': wallet_address,
        'chain_id': chain_id,
        'closed': include_closed,
        'closed_threshold': closed_threshold,
        'use_cache': use_cache
    }
    try:
        response = requests.get(BASE_URL_PROTOCOLS, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching protocol details: {e}")
        return None


def get_transaction_history(wallet_address: str, limit: int = 10):
    endpoint = f"{BASE_URL_HISTORY}/{wallet_address}"
    params = {'limit': limit}
    try:
        response = requests.get(endpoint, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching transaction history: {e}")
        return None

def get_current_value(wallet_address: str, chain_id: str):
    endpoint = f"{BASE_URL}/current_value"
    params = {'addresses': wallet_address, 'chain_id': chain_id}
    try:
        response = requests.get(endpoint, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error getting current value: {e}")
        return None

def get_profit_and_loss(wallet_address: str, chain_id: str, from_timestamp: str, to_timestamp: str):
    endpoint = f"{BASE_URL}/profit_and_loss"
    params = {
        'addresses': wallet_address,
        'chain_id': chain_id,
        'from_timestamp': from_timestamp,
        'to_timestamp': to_timestamp
    }
    try:
        response = requests.get(endpoint, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching profit and loss: {e}")
        return None

def get_token_details(wallet_address: str, chain_id: str):
    endpoint = f"{BASE_URL}/details"
    params = {'addresses': wallet_address, 'chain_id': chain_id}
    try:
        response = requests.get(endpoint, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error getting token details: {e}")
        return None

def delay(seconds: float):
    time.sleep(seconds)

if __name__ == "__main__":
    # response = get_profit_and_loss(EXAMPLE_WALLET, 1, '2024-01-01T00:00:00Z', '2025-01-T23:59:59Z')
    response = get_protocol_details(EXAMPLE_WALLET, 1)
    print(response)