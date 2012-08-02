#!/usr/bin/env python3
count = 0

def _print_brackets(N, M, String, Loc):
    if N == 0 and M == 0:
        global count
        count += 1
        print count, ''.join(String)
        return
    
    if N > 0:
        String[Loc] = '{'
        _print_brackets(N-1, M, String, Loc+1)
    
    if M > N:
        String[Loc] = '}'
        _print_brackets(N, M-1, String, Loc+1)

def print_brackets(N):
    global count
    count = 0
    String = ['' for i in xrange(0,N+N)]
    _print_brackets(N, N, String, 0)
    
# print bracket configurations (number of combinations is n'th catalan number = 1/(n+1) * [factorial(2n)/factorian(n)^2])
print_brackets(3)