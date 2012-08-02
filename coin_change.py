#!/usr/bin/env python3
def optimal_change(Amt, Currency, Inf):
    # array which contains optimal number of coins required for [0,1,...,Amt] amount
    num_coins = [0] # we need zero coins to give a change of 0 amount
    
    # array which contains the optimal change to reach that amount
    selected_change = [0]
    
    # start with 1 and go till Amt
    for i in xrange(1, Amt+1):
        
        # num_coins required for amount = i
        nc_i = Inf
        
        # selected change for amount = i 
        sc_i = Inf
        
        # iter over all coins in the currency
        for c in Currency:
            
            # if c is smaller than required amount and num coins to reach i-c is one less
            # than num coins (nc), then update local variables
            if i >= c and nc_i > num_coins[i-c] + 1:
                nc_i = num_coins[i-c] + 1
                sc_i = c
                
        # update optimal arrays
        num_coins.append(nc_i)
        selected_change.append(sc_i)
        
    # num_coins and selected_change can be used to print the coins required to get optimal change
    return [num_coins, selected_change]

def trace_optimal_solution(Amt, num_coins, selected_change):
    Amt0 = Amt
    
    # coins that are used to make the change for Amt
    coins = {}
    
    nc = num_coins[Amt]
    while nc > 0:
        # get the selected coin
        sc = selected_change[Amt]
        
        # add sc to coin map
        if coins.has_key(sc):
            coins[sc] += 1
        else:
            coins[sc] = 1
            
        # update Amt
        Amt = Amt - sc
        
        # get num coins require to attain Amt
        nc = num_coins[Amt]
    
    print "Optimal soln for", Amt0, "uses", num_coins[Amt0], "coins:", coins
    return coins
    
def greedy_change(Amt, Currency):
    Amt0 = Amt
    num_coins = 0
    coins = {}
    
    # we want to get as much change for max currency first, hence reverse sorting is required
    Currency = sorted(Currency, reverse=True)
    
    for c in Currency:
        # we can pay with c 
        if c <= Amt:
            
            # number of c coins to pay
            n = int(Amt/c)
            
            # decrement amount
            Amt = Amt - n * c
            
            # update vars
            num_coins += n
            coins[c] = n
            
    print "Greedy soln for", Amt0, "uses", num_coins, "coins:", coins
    return num_coins

# example of how to run the code
Inf = 100000
Currency = [1,4,5,21]
Amt = 12

print "Problem: We have currency =", Currency, "and want to make change for amount =", Amt, "\n"

# compute optimal solution for all amount <= Amt
[num_coins, selected_change] = optimal_change(Amt, Currency, Inf)

# print optimal solution for Amt
trace_optimal_solution(Amt, num_coins, selected_change)

# Computes and prints greedy soluton for Amt
greedy_change(12, Currency)