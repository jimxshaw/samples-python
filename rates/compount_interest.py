balance = 100.0
rate = 0.03

print(0, round(balance,2))
for n in range(1,11):
    balance = round(balance * (1 + rate), 2)
    print(n, round(balance,2))

def compound(balance, rate, num_periods):
    print(0, round(balance,2))
    for n in range(1,num_periods+1):
        balance = round( balance * (1 + rate), 2)
        print(n, balance)
    return balance

# Do NOT modify code above this line
# -----------------------

# Below is the function definition for compound_by_period. 
# Remove the comment before the function definition and 
# complete the function 

def compound_by_period(balance, rate, num_periods):
    # 1. Create a list that is initialized with the first balance 
    # 2. Write a for loop. Inside the loop, compute the yearly balance and append 
    # to the list
    # 3. Return the list
    result = [balance]

    for n in range(0, num_periods):
        bal = round(result[n] * (1 + rate), 2)
        result.append(bal)
    
    return result

# Make sure both functions output the same thing except for
# compound_by_period() returns a list.
print()
print(compound(balance, rate, 10))
result_list = compound_by_period(balance, rate, 10)
print(result_list)
print()

# Do NOT modify code below this line
# -----------------------------
def change_per_period(balances):
    for i in range(0,len(balances)-1):
         balances.append(balances[i+1] - balances[i])
    return balances

# Make sure compound_by_period() works with the
# change_per_period() function.
print(change_per_period(result_list)) 
