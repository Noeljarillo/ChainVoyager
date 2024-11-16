import json
import time
from web3 import Web3
from decimal import Decimal

w3 = Web3(Web3.HTTPProvider(f'https://api.securerpc.com/v1'))

def build_transaction_payload(
    action,
    web3,
    abi_path,
    contract_address,
    from_address,
    private_key,
    params
):
    """
    Builds transaction payloads for different actions.
    :param action: The action to perform ('swap', 'bridge', 'lend')
    :param web3: Web3 instance connected to a network
    :param abi_path: Path to the ABI file
    :param contract_address: Address of the contract
    :param from_address: Your wallet address
    :param private_key: Private key for signing transactions
    :param params: Dictionary of parameters required for the action
    :return: Raw transaction data ready to be signed and sent
    """

    
    with open(abi_path, 'r') as abi_file:
        contract_abi = json.load(abi_file)

    
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    
    nonce = web3.eth.get_transaction_count(from_address)
    gas_price = web3.eth.gas_price  
    chain_id = web3.eth.chain_id    

    if action == 'swap':
        
        token_in = params['token_in']
        token_out = params['token_out']
        amount_in = params['amount_in']
        amount_out_min = params['amount_out_min']
        to_address = params['to_address']
        deadline = params.get('deadline', int(time.time()) + 600)  
        txn = contract.functions.swapExactTokensForTokens(
            amount_in,
            amount_out_min,
            [token_in, token_out],
            to_address,
            deadline
        ).build_transaction({
            'from': from_address,
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': 250000,  
            'chainId': chain_id,
        })

    elif action == 'lend':
        raise NotImplementedError("Lend action is not implemented yet.")
    elif action == 'bridge':
        raise NotImplementedError("Bridge action is not implemented yet.")
    else:
        raise ValueError(f"Unsupported action: {action}")
    return txn