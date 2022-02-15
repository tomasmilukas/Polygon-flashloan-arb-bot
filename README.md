# Polygon flashloan WMATIC-DAI arbitrage bot (logic only)

Disclaimer: A lot of the same things are going to be repeated from the Polygon arb bot project (https://github.com/tomasmilukas/Polygon-arbitrage-bot). Moreover, this project is only the logic of the flashloan, and I have not executed it as a bot (yet).

Once I finished my basic bot, I wanted to delve into the flash loan concept asap! Moreover, after writing an article on DeFi lending (https://tomasmilukasblog.com/defi-lending-in-depth-fc5c77f9101d), there was nothing more I wanted to learn about :).

This is a simple flash loan arbitrage bot that trades WMATIC and DAI when there is a profitable opportunity on the Polygon chain between the following AMMs: QuickSwap and SushiSwap. The reason for deploying the bot on the polygon chain is because the gas fees are far lower than on the majority of other Layer 1 chains and also because it has fewer competitors going after the same opportunities. 

If you are curious about the bot's results, here are the relevant details: <br/>
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

The main two folders within this structure are the contracts and scripts folder. The contracts folder holds the main Solidity contracts necessary for the swaps and the scripts folder contains the Python files to deploy and call the contract.

The main contract file is **FlashloanV2.sol** which executes a swap from quick to sushi if the tradedirection is set to 1, and if it is set to any other number, it executes a trade from sushi to quick. The rest of the contracts are added for the swaps, or additional modifiers.

The **deployment_v2.py** is the file that will deploy the contract. However, the main execution file is **run_flash_loan_v2.py** which will call the flashloan() function within the smart contract.

If you wish to run this bot, you will need to fork the repo, then add a ".env" file with your private key and an Infura API that can call the Polygon Mainnet chain.

Once that is set up, you must deploy the contract with deployment_v2.py, fund the contract with the token you will be transacting, as Aave takes a fee and your transaction will lose money, and lastly run the run_flash_loan_v2.py. 

## Next steps

Besides the aforemationed next steps in my previous polygon arb project (mainly includes running BOR for faster execution speed), I plan to try out more sophisticated strategies such as triangular arbitrage to squeeze out the amount of profit possible from flash loans :).
