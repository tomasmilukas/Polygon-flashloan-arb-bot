from brownie import FlashloanV2, accounts, config, network, interface

MINIMUM_FLASHLOAN_WETH_BALANCE = 4000000000
ETHERSCAN_TX_URL = "https://mumbai.polygonscan.com/tx/{}"


def main():
    """
    Executes the funcitonality of the flash loan.
    """
    acct = accounts.add(config["wallets"]["from_key"])
    print("Getting Flashloan contract...")
    flashloan = FlashloanV2[len(FlashloanV2) - 1]
    weth = interface.WethInterface(config["networks"][network.show_active()]["dai"])
    print("Executing Flashloan...")
    tx = flashloan.flashloan(weth, 1, {"from": acct})
    print("You did it! View your tx here: " + ETHERSCAN_TX_URL.format(tx.txid))
    return flashloan