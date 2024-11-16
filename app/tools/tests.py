from get_yields import fetch_and_save_pools_data
from find_optimal import get_optimal_pools
import os
from Iinch_utils import get_protocol_details, get_token_details, get_transaction_history, get_profit_and_loss, get_current_value, delay

WALLET_ADDRESS = os.getenv("WALLET_ADDRESS_EXAMPLE")

CHAIN_ID = 1 
def test_fetch_and_save_pools_data():

    db_path = "../../db/pools_data.db"

    try:
        fetch_and_save_pools_data(db_path)
        print("Test passed: Data fetched and saved successfully.")
    except Exception as e:
        print(f"Test failed: {e}")

# Run the test
test_fetch_and_save_pools_data()

top_pools = get_optimal_pools(
    db_path='../../db/pools_data.db',
    exposure='single',
    stablecoin=True,
    chain='Ethereum',
    top_n=5
)

print(top_pools)

def test():
    print("Fetching ERC20 Tokens Current Value...")
    current_value = get_current_value(WALLET_ADDRESS, CHAIN_ID)
    if current_value:
        print("Current Value:")
        print(current_value)
    delay(2)  # Delay to respect rate limits

    from_timestamp = "2023-01-01T00:00:00Z"
    to_timestamp = "2023-01-31T23:59:59Z"

    print("\nFetching Profit and Loss (PnL) and ROI...")
    pnl = get_profit_and_loss(WALLET_ADDRESS, CHAIN_ID, from_timestamp, to_timestamp)
    if pnl:
        print("Profit and Loss:")
        print(pnl)
    delay(2)

    print("\nFetching Token Details...")
    token_details = get_token_details(WALLET_ADDRESS, CHAIN_ID)
    if token_details:
        print("Token Details:")
        print(token_details)
    delay(2)

    print("\nFetching Transaction History...")
    transaction_history = get_transaction_history(WALLET_ADDRESS, limit=10)
    if transaction_history:
        print("Transaction History:")
        print(transaction_history)
    delay(2)

    print("\nFetching Protocol Details...")
    protocol_details = get_protocol_details(WALLET_ADDRESS, CHAIN_ID, include_closed=True, closed_threshold=10, use_cache=False)
    if protocol_details:
        print("Protocol Details:")
        print(protocol_details)

test()

