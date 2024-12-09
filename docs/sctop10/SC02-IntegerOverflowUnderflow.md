---
id: SC02
title: Integer Overflow and Underflow
hide:
  - toc
---

## Vulnerability: Integer Overflow and Underflow

### Description:
Ethereum Virtual Machine (EVM) defines fixed-size data types for integers. This implies that the range of numbers that an integer variable can represent is finite.For instance, a “uint8” (unsigned integer of 8 bits; i.e., non-negative) can only store integers that fall between 0 and 255. The outcome of trying to store any value greater than 255 into an “uint8” will lead to an overflow. Similarly, the outcome of subtracting “1” from “0” will produce 255. This is called underflow.When an arithmetic operation exceeds or falls short of a type’s maximum or minimum size, an overflow or underflow occurs.For signed integers, the outcome will be a bit different. If we try subtracting “1” from an int8 whose value is -128, we get 127. This is because signed int types, which may represent negative values, start over once we reach the highest negative value.Two straightforward examples of this behavior include periodic mathematical functions (adding 2 to the argument of sin leaves the value intact) and odometers in automobiles, which track distance traveled (they reset to 000000 after the maximum number, i.e., 999999, is exceeded).

***Important Note:-
In Solidity `0.8.0` and above, the compiler automatically handles checking for overflows and underflows in arithmetic operations, reverting the transaction if an overflow or underflow occurs.
Solidity `0.8.0` also introduces the `unchecked` keyword, which allows developers to perform arithmetic operations without these automatic checks, explicitly permitting overflow without reverting. This can be particularly useful for optimizing gas usage in cases where overflow is not a concern or where the wraparound behavior is desired, similar to how arithmetic behaved in earlier versions of Solidity.***

### Example:
```
// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract TimeWrapVault {
    mapping(address => uint256) public accountBalances;
    mapping(address => uint256) public withdrawalUnlockTime;

    // Allows anyone to deposit ETH and set a lock time
    function depositFunds() external payable {
        accountBalances[msg.sender] += msg.value;
        withdrawalUnlockTime[msg.sender] = block.timestamp + 1 weeks;
    }

    // Vulnerable to overflow, the user could pass a very large value causing overflow
    function extendLockTime(uint256 _additionalSeconds) public {
        withdrawalUnlockTime[msg.sender] += _additionalSeconds;
    }

    // Allows withdrawals only if the current time is greater than the lock time
    function releaseFunds() public {
        require(accountBalances[msg.sender] > 0, "Insufficient funds");
        require(block.timestamp > withdrawalUnlockTime[msg.sender], "Lock time not expired");

        uint256 withdrawalAmount = accountBalances[msg.sender];
        accountBalances[msg.sender] = 0;

        (bool successfulWithdrawal,) = msg.sender.call{value: withdrawalAmount}("");
        require(successfulWithdrawal, "Failed to send Ether");
    }
}

```
### Impact:
- An attacker could exploit such vulnerabilities to artificially increase account balances or token amounts, potentially allowing them to withdraw more funds than they legitimately own.
- An attacker might alter the intended flow of contract logic, leading to unauthorized actions like stealing assets or minting an excessive number of tokens.

### Remediation:
- The simplest approach is to use Solidity compiler version 0.8.0 or higher, as it automatically handles overflow and underflow checks.
- Make Use of the latest Safe Math Libraries: For the Ethereum community, OpenZeppelin has done a fantastic job creating and auditing secure libraries. Its SafeMath library, in particular, can be used to prevent under/overflow vulnerabilities. It provides functions like add(), sub(), mul(), etc., that carry out basic arithmetic operations and automatically revert if an overflow or underflow occurs.

### Examples of Smart Contracts that fell victim to Integer Overflow and Underflow Attacks:
1. [PoWH Coin Ponzi Scheme](https://etherscan.io/token/0xa7ca36f7273d4d38fc2aec5a454c497f86728a7a#code) : A Comprehensive [Hack Analysis](https://blog.solidityscan.com/integer-overflow-and-underflow-in-smart-contracts-9598032b5a99)
2. [Poolz Finance](https://bscscan.com/address/0x8bfaa473a899439d8e07bf86a8c6ce5de42fe54b#code) : A Comprehensive [Hack Analysis](https://blog.solidityscan.com/poolz-finance-hack-analysis-still-experiencing-overflow-fcf35ab8a6c5)