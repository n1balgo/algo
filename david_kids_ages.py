#!/usr/bin/env python

def print_ages(kids_ages):
    """ Print kids ages, ignore 0 that are towards the end in the kids_ages array """
    for age in kids_ages:
        if age == 0: break
        print age,
    print

def check_ages(kids_ages):
    """ Check age constraint, ignore 0 that are towards the end in the kids_ages array """
    s = 0
    p = 1
    
    # compute sum of ages and product of ages
    for age in kids_ages:
        if age == 0: break
        s += age
        p *= age
    
    # check for constraint sum^2 = product (of ages)
    if s*s == p:
        return True
    else:
        return False
    
def find_ages(kids_ages, num_kids):
    if num_kids == 0:
        least_age = 13
    else:
        # check kids ages
        if check_ages(kids_ages):
            print "Ages that satisfy constraint:",
            print_ages(kids_ages)
        
        # david has less than 7 kids
        if num_kids >= 7:
            return
        
        # pick the smallest age 
        least_age = kids_ages[num_kids-1]
        
    # add kid with different ages to kids_ages
    for age in xrange(2, least_age):
        # add a kid with age = age
        kids_ages[num_kids] = age
        
        # find age recursively
        find_ages(kids_ages, num_kids+1)
        
    # undo the added kid
    kids_ages[num_kids] = 0

kids_ages = [0 for i in xrange(0,7)]
find_ages(kids_ages, 0)