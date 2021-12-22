// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.6.0;

interface marketplace {

    function settleAuction(address,address,uint256,uint256,uint256) external;
}
