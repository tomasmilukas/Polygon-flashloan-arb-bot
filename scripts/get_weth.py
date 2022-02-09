from brownie import accounts, config, network, interface


def main():
    """
    Runs the get_weth function to get WETH
    """
    get_weth()


def get_weth():
    """
    Mints WETH by depositing ETH.
    """
    acct = accounts.add(
        config["wallets"]["from_key"]
    )  # add your keystore ID as an argument to this call
    weth = interface.WethInterface(config["networks"]["polygon-test"]["wmatic"])
    tx = weth.deposit({"from": acct, "value": 10000000000000000})
    print("Received WMATIC")
    return tx
