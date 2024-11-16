from web3 import Web3
import json

def generate_aave_deposit_calldata(
    lending_pool_address: str,
    asset_address: str,
    amount: int,
    on_behalf_of: str,
    referral_code: int = 0
) -> str:
    """
    Generates calldata for the Aave LendingPool deposit function.

    :param lending_pool_address: The address of the Aave LendingPool contract.
    :param asset_address: The address of the ERC20 asset to deposit.
    :param amount: The amount of the asset to deposit (in wei).
    :param on_behalf_of: The address on whose behalf the deposit is made.
    :param referral_code: Referral code for the deposit (default is 0).
    :return: Hexadecimal string of the calldata.
    """

    with open('./abis/aave_usdt.json', 'r') as abi_file:
        lending_pool_abi = json.load(abi_file)

    w3 = Web3()

    lending_pool_contract = w3.eth.contract(
        address=lending_pool_address,
        abi=lending_pool_abi
    )

    calldata = lending_pool_contract.encodeABI(
        fn_name='deposit',
        args=[
            asset_address,
            amount,
            on_behalf_of,
            referral_code
        ]
    )

    return calldata
