#!/usr/bin/env python3
count = 0

def _permute_chars(String, Loc):
    # get string length
    l = len(String)
    
    # reached the end of the String, nothing more to permute
    if l == Loc:
        global count
        count += 1
        print count, ''.join(String)
        return
    
    # get charater to be swapped
    c = None
    
    # do a cyclic rotation of String by 1,
    # Intuition behind cyclic shift is that it leaves the subarray (Loc+1 to l) sorted
    # a simple swap used in _permute_unique_chars does not ensure that
    for i in xrange(Loc, l):
        # same character, avoid duplicate permutations
        if c == String[i]: continue
        
        # swap character at Loc and i
        c = String[i]
        String[i] = String[Loc]
        String[Loc] = c
        
        # recursively permute
        _permute_chars(String, Loc+1)
    
    # after the end of above loop, string is cyclically shifted by 1, undo this shift
    for i in xrange(Loc,l-1):
        String[i] = String[i+1]
    String[l-1] = c

def permute_chars(perm_str):
    # set global counter to 0
    global count
    count = 0
    
    # make a array from string (as string in non-mutable)
    string = [perm_str[i] for i in xrange(0,len(perm_str))]
    
    # sort string
    string = sorted(string)
    
    # permute string array
    print "Permuting duplicated chars:", perm_str
    _permute_chars(string, 0)

# permute duplicated chars
permute_chars("abab")