pragma solidity ^0.6.6;

import "./aave/FlashLoanReceiverBaseV2.sol";
import "../../interfaces/v2/ILendingPoolAddressesProviderV2.sol";
import "../../interfaces/v2/ILendingPoolV2.sol";
import "./IUniswapV2Router02.sol";
import "./IWETH.sol";



contract FlashloanV2 is FlashLoanReceiverBaseV2, Withdrawable {

    struct TradeDirection{  
        uint directionNumber;
    }

    IUniswapV2Router02 quick_router;
    IUniswapV2Router02 sushi_router;
    IERC20 usdc;
    IWETH wmatic;
    TradeDirection public tradeDirection;
    uint direction = 1;

    constructor(
        address _addressProvider,
        address sushiAddress,
        address quickAddress,
        address wmaticAddress,
        address usdcAddress) FlashLoanReceiverBaseV2(_addressProvider) public {
        sushi_router = IUniswapV2Router02(sushiAddress);
        quick_router = IUniswapV2Router02(quickAddress);
        wmatic = IWETH(wmaticAddress);
        usdc = IERC20(usdcAddress);
        }

    /**
     * @dev This function must be called only be the LENDING_POOL and takes care of repaying
     * active debt positions, migrating collateral and incurring new V2 debt token debt.
     *
     * @param assets The array of flash loaned assets used to repay debts.
     * @param amounts The array of flash loaned asset amounts used to repay debts.
     * @param premiums The array of premiums incurred as additional debts.
     * @param initiator The address that initiated the flash loan, unused.
     * @param params The byte array containing, in this case, the arrays of aTokens and aTokenAmounts.
     */
    function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address initiator,
        bytes calldata params
    )
        external
        override
        returns (bool)
    {
        uint256 usdcBalance = usdc.balanceOf(address(this));
        if (tradeDirection.directionNumber == 1){
            quickToSushi(usdcBalance);
         } 
         else {
            sushiToQuick(usdcBalance);
            }
        
        // Approve the LendingPool contract allowance to *pull* the owed amount
        for (uint i = 0; i < assets.length; i++) {
            uint amountOwing = amounts[i].add(premiums[i]);
            IERC20(assets[i]).approve(address(LENDING_POOL), amountOwing);
        }
        
        return true;
    }



    function _flashloan(address[] memory assets, uint256[] memory amounts) internal {
        address receiverAddress = address(this);

        address onBehalfOf = address(this);
        bytes memory params = "";
        uint16 referralCode = 0;

        uint256[] memory modes = new uint256[](assets.length);

        // 0 = no debt (flash), 1 = stable, 2 = variable
        for (uint256 i = 0; i < assets.length; i++) {
            modes[i] = 0;
        }

        LENDING_POOL.flashLoan(
            receiverAddress,
            assets,
            amounts,
            modes,
            onBehalfOf,
            params,
            referralCode
        );
    }

    /*
     *  Flash loan 1000000000000000000 wei (1 ether) worth of `_asset`
     */
    function flashloan(address _asset, uint _direction) public onlyOwner {
        tradeDirection.directionNumber = _direction;
        bytes memory data = "";
        uint amount = 1 ether;

        address[] memory assets = new address[](1);
        assets[0] = _asset;

        uint256[] memory amounts = new uint256[](1);
        amounts[0] = amount;

        _flashloan(assets, amounts);
    }

    function quickToSushi(uint256 usdcBalance) internal {
        // USDC -> WMATIC on quickswap
            usdc.approve(address(quick_router), usdcBalance);
            address[] memory direction_quick = new address[] (2);
            direction_quick[0] = address(usdc);
            direction_quick[1] = address(wmatic);
            uint[] memory minOut_quick = quick_router.getAmountsOut(usdcBalance, direction_quick);
            uint minOut_quick1 = minOut_quick[0] * 50;
            uint minOut_quick2 = minOut_quick1 / 100;
            quick_router.swapExactTokensForETH(usdcBalance, minOut_quick2, direction_quick, address(this), now);
            
            // WMATIC -> USDC on sushi
            address[] memory direction_sushi = new address[] (2);
            direction_sushi[0] = address(wmatic);
            direction_sushi[1] = address(usdc);
            uint[] memory minOut_sushi = sushi_router.getAmountsOut(usdcBalance, direction_sushi);
            uint minOut_sushi1 = minOut_sushi[0] * 50;
            uint minOut_sushi2 = minOut_sushi1 / 100;
            sushi_router.swapExactETHForTokens{value: address(this).balance}(minOut_sushi2, direction_sushi, address(this), now);
    }

    function sushiToQuick(uint256 usdcBalance) internal {
           // USDC -> WMATIC on sushiswap
            usdc.approve(address(sushi_router), usdcBalance);
            address[] memory direction_sushi = new address[] (2);
            direction_sushi[0] = address(usdc);
            direction_sushi[1] = address(wmatic);
            uint[] memory minOut_sushi = sushi_router.getAmountsOut(usdcBalance, direction_sushi);
            uint minOut_sushi1 = minOut_sushi[0] * 50;
            uint minOut_sushi2 = minOut_sushi1 / 100;
            sushi_router.swapExactTokensForETH(usdcBalance, minOut_sushi2, direction_sushi, address(this), now);

            // WMATIC -> USDC on quickswap
            address[] memory direction_quick = new address[] (2);
            direction_quick[0] = address(wmatic);
            direction_quick[1] = address(usdc);
            uint[] memory minOut_quick = quick_router.getAmountsOut(usdcBalance, direction_quick);
            uint minOut_quick1 = minOut_quick[0] * 50;
            uint minOut_quick2 = minOut_quick1 / 100;
            quick_router.swapExactETHForTokens{value: address(this).balance}(minOut_quick2, direction_quick, address(this), now);
    }


    function withdrawToken(address _tokenContract, uint256 _amount) external onlyOwner {
    IERC20 tokenContract = IERC20(_tokenContract);
    tokenContract.transfer(msg.sender, _amount);
    }

    function withdrawAll(address _tokenAddress) external onlyOwner{
        IERC20 tokenContract = IERC20(_tokenAddress);
        uint256 totalBalance = tokenContract.balanceOf(address(this));
        tokenContract.transfer(msg.sender, totalBalance);
    }
}