#!/usr/bin/env python3

path_count = 1

def print_regular_paths(x, y, path):
    if x == 0 and y == 0:
        # print the path
        global path_count
        print path_count, path
        path_count += 1
        return
    
    # check if we can go right
    if x > 0:
        # print paths after taking a right
        print_regular_paths(x-1, y, path+"right, ")
    
    # check if we can go up
    if y > 0:
        # print paths after taking a up
        print_regular_paths(x, y-1, path+"up, ")

def print_bounded_paths(x, y, n, m, path):
    if x == n and y == m:
        # print the path
        global path_count
        print path_count, path
        path_count += 1
        return
    
    # check if we can go right    
    if x < n:
        # print paths after taking a right
        print_bounded_paths(x+1, y, n, m, path+"right, ")
    
    # check if we can go up, number of up should be less than number of right for this
    if y < m and y < x:
        # print paths after taking a up
        print_bounded_paths(x, y+1, n, m, path+"up, ")
    

def print_diagonal_paths(x, y, n, m, path):
    if x == n and y == m:
        # print the path
        global path_count
        print path_count, path
        path_count += 1
        return
    
    # check if we can go right
    if x < n:
        # print paths after taking a right
        print_diagonal_paths(x+1, y, n, m, path+"right, ")
    
    # check if we can go up
    if y < m:
        # print paths after taking a up
        print_diagonal_paths(x, y+1, n, m, path+"up, ")
        
    # check if we can take a diagonal, i.e. we should be able to go up and right atleast one
    if x < n and y < m:
        # print paths after taking a diagonal
        print_diagonal_paths(x+1, y+1, n, m, path+"diagonal, ")

def print_paths(pathType, n, m):
    global path_count
    if pathType == "regular":
        print "printing regular paths"
        path_count = 1
        print_regular_paths(n, m, "")
        print "="*10
    elif pathType == "bounded":
        print "printing bounded paths"
        path_count = 1
        print_bounded_paths(0, 0, n, m, "")
        print "="*10
    else:
        print "printing diagonal paths"
        path_count = 1
        print_diagonal_paths(0,0, n, m, "")
        print "="*10

n = 3
m = 2
print_paths("regular", n, m)
print_paths("bounded", n, m)
print_paths("diagonal", n, m)