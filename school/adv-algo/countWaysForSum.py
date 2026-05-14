def countWaysToMakeSum(coins, numDenominations, remainingSum, wayCount, callDepth=0):
    """
    Counts the number of ways to make remainingSum using the first
    numDenominations coins from the coins list.

    coins            : list of coin denominations e.g. [1, 2, 3]
    numDenominations : how many denominations we're currently allowed to use
    remainingSum     : the sum we still need to make
    wayCount         : 2D memoization table  [numDenominations][remainingSum]
    callDepth        : just for pretty indented printing — not part of the algorithm
    """

    indent = "  " * callDepth  # visual indentation to show recursion depth

    print(f"\n{indent}>>> ENTERING call: numDenominations={numDenominations}, remainingSum={remainingSum}")
    print(f"{indent}    Coins available: {coins[:numDenominations]}")

    # -------------------------------------------------------------------------
    # BASE CASE 1 — remaining sum is zero
    # There is exactly one way to make zero: use no coins at all
    # -------------------------------------------------------------------------
    if remainingSum == 0:
        print(f"{indent}    BASE CASE HIT: remainingSum == 0 → return 1 (empty combination counts)")
        return 1

    # -------------------------------------------------------------------------
    # BASE CASE 2 — no denominations left but sum is still positive
    # Impossible to make a positive sum with zero coins available
    # -------------------------------------------------------------------------
    if numDenominations == 0:
        print(f"{indent}    BASE CASE HIT: numDenominations == 0 → return 0 (no coins left, sum still {remainingSum})")
        return 0

    # -------------------------------------------------------------------------
    # MEMOIZATION CHECK — have we already solved this exact subproblem?
    # If so, return the cached answer immediately without recursing further
    # -------------------------------------------------------------------------
    if wayCount[numDenominations][remainingSum] is not None:
        cachedAnswer = wayCount[numDenominations][remainingSum]
        print(f"{indent}    CACHE HIT: wayCount[{numDenominations}][{remainingSum}] already = {cachedAnswer} → returning immediately")
        return cachedAnswer

    # -------------------------------------------------------------------------
    # THE CURRENT COIN
    # coins is 1-indexed in the algorithm but Python lists are 0-indexed,
    # so coins[numDenominations - 1] gives us the current denomination
    # -------------------------------------------------------------------------
    currentCoinValue = coins[numDenominations - 1]
    print(f"{indent}    Current coin being considered: coins[{numDenominations}-1] = {currentCoinValue}")

    # -------------------------------------------------------------------------
    # CASE A — current coin is too large to fit into remainingSum
    # We cannot use it at all, so skip it and try with one fewer denomination
    # -------------------------------------------------------------------------
    if currentCoinValue > remainingSum:
        print(f"{indent}    CASE A: coin value {currentCoinValue} > remainingSum {remainingSum} → coin too big, skip it")
        print(f"{indent}    Recursing with numDenominations={numDenominations - 1}, remainingSum={remainingSum}")

        wayCount[numDenominations][remainingSum] = countWaysToMakeSum(
            coins,
            numDenominations - 1,   # drop this denomination
            remainingSum,           # sum unchanged
            wayCount,
            callDepth + 1
        )

    # -------------------------------------------------------------------------
    # CASE B — current coin fits
    # Two mutually exclusive choices that together cover ALL possibilities:
    #   Choice 1: Don't use this denomination at all
    #   Choice 2: Use this denomination at least once (keep it available for reuse)
    # -------------------------------------------------------------------------
    else:
        print(f"{indent}    CASE B: coin value {currentCoinValue} <= remainingSum {remainingSum} → coin fits, split into 2 choices")

        print(f"\n{indent}    --- Choice 1: SKIP coin {currentCoinValue} entirely ---")
        print(f"{indent}    Recursing with numDenominations={numDenominations - 1}, remainingSum={remainingSum}")
        waysWithoutThisCoin = countWaysToMakeSum(
            coins,
            numDenominations - 1,   # move on without this coin
            remainingSum,           # sum unchanged
            wayCount,
            callDepth + 1
        )

        print(f"\n{indent}    --- Choice 2: USE coin {currentCoinValue} at least once ---")
        print(f"{indent}    Recursing with numDenominations={numDenominations}, remainingSum={remainingSum - currentCoinValue}")
        waysUsingThisCoin = countWaysToMakeSum(
            coins,
            numDenominations,                    # keep this coin available (reusable)
            remainingSum - currentCoinValue,     # reduce remaining sum
            wayCount,
            callDepth + 1
        )

        print(f"\n{indent}    Combining: waysWithoutThisCoin={waysWithoutThisCoin} + waysUsingThisCoin={waysUsingThisCoin}")
        wayCount[numDenominations][remainingSum] = waysWithoutThisCoin + waysUsingThisCoin

    # -------------------------------------------------------------------------
    # STORE AND RETURN
    # Cache the result so we never compute this (numDenominations, remainingSum)
    # pair again
    # -------------------------------------------------------------------------
    result = wayCount[numDenominations][remainingSum]
    print(f"{indent}    STORING: wayCount[{numDenominations}][{remainingSum}] = {result}")
    print(f"{indent}<<< RETURNING {result} for numDenominations={numDenominations}, remainingSum={remainingSum}")
    return result


def solve(coins, targetSum):
    """
    Wrapper that sets up the memoization table and kicks off the recursion.
    """
    numDenominations = len(coins)

    # Initialize the 2D wayCount table with all None values
    # Size: (numDenominations + 1) rows  x  (targetSum + 1) columns
    # The +1 on each dimension is because we use 1-based indexing for denominations
    # and we need a slot for sum=0 as the base case
    wayCount = [[None] * (targetSum + 1) for _ in range(numDenominations + 1)]

    print("=" * 60)
    print(f"PROBLEM: coins={coins}, targetSum={targetSum}")
    print(f"Table size: {numDenominations + 1} rows x {targetSum + 1} columns")
    print("=" * 60)

    answer = countWaysToMakeSum(coins, numDenominations, targetSum, wayCount)

    print("\n" + "=" * 60)
    print(f"FINAL ANSWER: {answer} ways to make sum {targetSum} using coins {coins}")
    print("=" * 60)

    # Print the final memoization table so you can see what got cached
    print("\nFINAL MEMOIZATION TABLE (rows=numDenominations, cols=sum):")
    print("     ", end="")
    for col in range(targetSum + 1):
        print(f"  S={col}", end="")
    print()
    for row in range(numDenominations + 1):
        print(f"d={row} |", end="")
        for col in range(targetSum + 1):
            val = wayCount[row][col]
            print(f"  {'?' if val is None else val}  ", end="")
        print()

    return answer


# =============================================================================
# RUN EXAMPLE 1 — small and traceable by hand
# coins = [1, 2, 3], targetSum = 4
# Expected output: 4
# The 4 ways are: {1,1,1,1}, {1,1,2}, {2,2}, {1,3}
# =============================================================================
solve([1, 2, 3], 4)