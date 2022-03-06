# Polygon flashloan WMATIC-DAI arbitrage bot 

Disclaimer: Quite some things are repeated from the Polygon arb bot project (https://github.com/tomasmilukas/Polygon-arbitrage-bot). Moreover, this project is not an automated bot strategy, you have to manually trigger it.

This is a flash loan arbitrage bot that trades WMATIC and DAI on the Polygon chain between the following AMMs: QuickSwap and SushiSwap.

If you are curious about the bot's results/workings, here are the relevant details: <br/>
The arbitrage contracts address: 0x27BF8102E6f65Bf0436F176D587981f3Bbf270C1 <br/>
The polygonscan link to the contract: https://polygonscan.com/address/0x27bf8102e6f65bf0436f176d587981f3bbf270c1 <br/>

## Table of contents

* [Technologies](#technologies)
* [Setup](#setup)
* [Next steps](#next-steps)

## Technologies

The contracts were coded with **Solidity**. <br/>
The bot execution was done with **Python**. <br/>
The API calls were done on **Infura**. <br/>
The Flash Loan provider was **Aave V2**. <br/>
	
## Setup

The main two folders within this structure are the contracts (v2 folder) and scripts folder. The v2 folder holds the main Solidity contracts necessary for the swaps and the scripts folder contains the Python files to deploy and call the contract.

The main contract file is **FlashloanV2.sol** which executes a swap from quick to sushi if the tradedirection is set to 1, and if it is set to any other number, it executes a trade from sushi to quick. The rest of the contracts are added for the swaps, or additional modifiers.

The **deployment_v2.py** is the file that will deploy the contract. Once that is done, you must manually send some DAI to the contract to be able to call the flashloan function. Because you will not be calling the flashloan on a profitable opportunity, it will cost you some funds due to the Aave fee, hence, if there aren't any funds in the contract it will always revert. For the main execution, you must run the **run_bot.py** file which calls the flashloan() function with web3.py within the smart contract. There are instructions inside the contract, but they will be repeated below.

Once you have forked this repo, within the scripts folder, add a ".env" file where you will specify your Infura web project ID and your private key (take note of the 0x addition). Moreover, you must create a config.py file and add in your infura API and your private key (additional details in the run_bot.py file). Take note that both of these files must be within the same directory, and you must run the following command "source .env" to provide the .env details for the project to use. Lastly, you must change the "sender_address" variable to your own address and the "floashloan_address" variable to your deployed contract address. Other things to double check are if you correctly added your private keys, if your Infura API is linked to polygon mainnet (not mumbai or ethereum testnet) and if you have correctly set up the .env and config.py files. 

If you have executed the steps above correctly, idm if you sent me DMs or questions, but please do some of your own solving as well :)!

## Next steps

Besides the aforemationed next steps in my previous polygon arb project (mainly includes running BOR for faster execution speed), I plan to try out more sophisticated strategies such as triangular arbitrage to squeeze out the amount of profit possible from flash loans :).
