#!/usr/bin/env python3
count = 0

def _permute_unique_chars(String, Loc):
    # get string length
    l = len(String)
    
    # reached the end of the String, nothing more to permute
    if l == Loc:
        global count
        count += 1
        print count, ''.join(String)
        return
    
    # get charater at position = Loc
    c = String[Loc]
    
    # permute the character at position = Loc with characters at position > Loc
    for i in xrange(Loc, l):
        # swap character at Loc and i
        String[Loc] = String[i]
        String[i] = c
        
        # recursively permute
        _permute_unique_chars(String, Loc+1)
        
        # undo the swap at depth and i
        String[i] = String[Loc]
        String[Loc] = c

def permute_unique_chars(perm_str):
    # set global counter to 0
    global count
    count = 0
    
    # make a array from string (as string in non-mutable)
    string = [perm_str[i] for i in xrange(0,len(perm_str))]
    
    # permute string array
    print "Permuting unique chars:", perm_str
    _permute_unique_chars(string, 0)

# permute unique chars
permute_unique_chars("abc")
