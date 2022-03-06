from web3 import Web3, exceptions

import requests
import json
import config

# Create a config.py file and add in two variables:
# 1.Your private key in brackets, should be called as such: private_key="YOUR_PRIVATE_KEY"
# 2.Add the polygon matic api from infura or alchemy, should be called as such: matic_api="YOUR_API"
# Make sure the config.py file is in the same directory.

# Make sure you also have your .env file in the same directory as run_bot.py. The .env file should have two variables:
# export WEB3_INFURA_PROJECT_ID="YOUR_INFURA_ID", which connects to your infura account
# export PRIVATE_KEY="0xYOUR_PRIVATE_KEY", which connects to your wallet. Make sure to keep the "" (brackets) and that you have 0x before your private key.

matic = config.matic_api
web3 = Web3(Web3.HTTPProvider(matic))

# Address definitions. Change the sender_address to your own address and the flashloan_address to your deployed contract address.
wmatic_address = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"
usdc_address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
flashloan_address = "0x27BF8102E6f65Bf0436F176D587981f3Bbf270C1"
sender_address = "0xDB3046E0D2557996252c2d49534eA333A0FEBC74"
dai_address = "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063"

flashloan_abi = json.loads('[ { "inputs": [ { "internalType": "address", "name": "_addressProvider", "type": "address" }, { "internalType": "address", "name": "sushiAddress", "type": "address" }, { "internalType": "address", "name": "quickAddress", "type": "address" }, { "internalType": "address", "name": "wmaticAddress", "type": "address" }, { "internalType": "address", "name": "usdcAddress", "type": "address" } ], "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "_from", "type": "address" }, { "indexed": true, "internalType": "address", "name": "_assetAddress", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "LogWithdraw", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "previousOwner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "OwnershipTransferred", "type": "event" }, { "inputs": [], "name": "ADDRESSES_PROVIDER", "outputs": [ { "internalType": "contract ILendingPoolAddressesProviderV2", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "LENDING_POOL", "outputs": [ { "internalType": "contract ILendingPoolV2", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address[]", "name": "assets", "type": "address[]" }, { "internalType": "uint256[]", "name": "amounts", "type": "uint256[]" }, { "internalType": "uint256[]", "name": "premiums", "type": "uint256[]" }, { "internalType": "address", "name": "initiator", "type": "address" }, { "internalType": "bytes", "name": "params", "type": "bytes" } ], "name": "executeOperation", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "_asset", "type": "address" }, { "internalType": "uint256", "name": "_direction", "type": "uint256" } ], "name": "flashloan", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "owner", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "tradeDirection", "outputs": [ { "internalType": "uint256", "name": "directionNumber", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "_assetAddress", "type": "address" } ], "name": "withdraw", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "_tokenAddress", "type": "address" } ], "name": "withdrawAll", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "_tokenContract", "type": "address" }, { "internalType": "uint256", "name": "_amount", "type": "uint256" } ], "name": "withdrawToken", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "stateMutability": "payable", "type": "receive" } ]')

# Contract definitions

contract_flashloan = web3.eth.contract(address=flashloan_address,abi=flashloan_abi)

nonce = web3.eth.get_transaction_count(sender_address)

# Before calling, remember to deposit some funds into the contract, otherwise this function will not work! You can send it manually via metamask or another wallet by inputting the address.

flashloan_tx = contract_flashloan.functions.flashloan(
    dai_address,
    1
    ).buildTransaction({
    'from': sender_address,
    'nonce': nonce
    })

signature = web3.eth.account.sign_transaction(flashloan_tx, private_key = config.private_key)
tx_token = web3.eth.send_raw_transaction(signature.rawTransaction)
print(web3.toHex(tx_token))

# Call this if you want to withdraw the funds you have deposited

# withdraw_tx = contract_flashloan.functions.withdrawAll(
#     dai_address
#     ).buildTransaction({
#     'from': sender_address,
#     'nonce': nonce
#     })

# signature = web3.eth.account.sign_transaction(withdraw_tx, private_key = config.private_key)
# tx_token = web3.eth.send_raw_transaction(signature.rawTransaction)
# print(web3.toHex(tx_token))