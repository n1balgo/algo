#!/usr/bin/env python3

# input array
arr = [2, 4, 3, 7, 3, 0, 8, 4, 11, 1]
print "Initial array =", arr, "\n"

# number of comparisons
num_compare = 0

# indexes that are to be compared    
idx = range(0,len(arr))

# list of knockout for all elements
knockout = [[] for i in idx]

# play tournaments, until we have only one node left
while len(idx) > 1:
    
    # index of nodes that win this tournament
    idx1 = []
    
    # nodes in idx odd, if yes then last automatically goes to next round
    odd = len(idx) % 2
    
    # iterate over even indexes, as we do a paired tournament
    for i in xrange(0, len(idx) - odd, 2):
        
        # first index
        i0 = idx[i]
        
        # second index
        i1 = idx[i+1]
        
        # update num comparisons
        num_compare += 1
        
        # perform tournament
        if arr[i0] < arr[i1]:
            # i0 qualifies for next round
            idx1.append(i0)
            
            # add arr[i1] to knockout list of i0
            knockout[i0].append(arr[i1])
        else:
            # i1 qualifies for next round
            idx1.append(i1)
            
            # add arr[i0] to knockout list of i1
            knockout[i1].append(arr[i0])
        
    # last element goes to next round
    if odd == 1:
        idx1.append(idx[i+2])
            
    # perform new tournament
    idx = idx1

print "Smallest element =", arr[idx[0]]
print "Total comparisons =", num_compare
print "Nodes knocked off by the smallest =", knockout[idx[0]], "\n"

# compute smallest
a = knockout[idx[0]]
if len(a) > 0:
    v = a[0]
    for i in xrange(1,len(a)):
        num_compare += 1
        if v > a[i]: v = a[i]
        
    print "Second smallest element =", v
    print "Total comparisons =", num_compare