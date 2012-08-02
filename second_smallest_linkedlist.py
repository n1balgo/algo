#!/usr/bin/env python3

class Node:
    def __init__(self, val):
        # value at this node
        self.val = val
        
        # sibling ptr for linked list
        self.sibling = None
        
        # child ptr, maintains nodes knocked by this node
        self.child = None

def create_linked_list(Arr):
    """ Create a linked list from input array """
    
    # check if array is empty or not
    if len(Arr) == 0:
        return None
    
    # put first array value as head of linked list
    head = Node(Arr[0])
    
    # vars for linked list
    prev = head
    curr = None
    
    # read remaining array and set sibling ptrs
    for i in xrange(1,len(Arr)):
        # create a new node
        curr = Node(Arr[i])
        
        # set prev's sibling
        prev.sibling = curr
        
        # update prev pointer
        prev = curr
        
    return head

def print_linked_list(head):
    """ print linked list pointed to by head """
    while head != None:
        print head.val, 
        head = head.sibling
    print
    
def print_child_list(head):
    """ print child list ponted to by head """
    while head != None:
        print head.val, 
        head = head.child
    print

num_compare = 0
def get_smallest(list_head):
    """ get smallest element recursively, maintaining a list of nodes knocked off by the smallest """
    global num_compare
    
    # create a new list of nodes that are smaller than their sibling (do for alternate siblings)
    head = None
    curr = None
    num = 0
    
    # vars for current list
    ptrprev = list_head
    ptr0 = list_head
    
    while ptr0 != None:
        # get ptr0's sibling
        ptr1 = ptr0.sibling
        
        if ptr1 != None:
            ' update number of comparisons '
            num_compare += 1
            
            # compare ptr0 and ptr1
            if ptr0.val <= ptr1.val:
                # ptr0 knocks ptr1, so move ptr0 above ptr1
                # set its sibling to None
                # set ptr1's child to ptr0's child (we need all nodes knocked by ptr0)
                # set ptr0's child to ptr1
                
                # update sibling pointers
                ptr0.sibling = None
                
                # update child pointers
                ptr1.child = ptr0.child
                ptr0.child = ptr1
                
                # swap ptrs, for while loop to move to next node
                temp = ptr0
                ptr0 = ptr1
                ptr1 = temp
            else:
                # ptr1 knocks ptr0
                # set ptr0's sibling as ptr1's sibling (so while loop can go to it)
                # set ptr1's sibling to None
                # set ptr0's child as ptr1's child (we need all nodes knocked by ptr1)
                # set ptr1's child to ptr0
                
                # update sibling pointers
                ptr0.sibling = ptr1.sibling
                ptr1.sibling = None
                
                # update child pointers
                ptr0.child = ptr1.child
                ptr1.child = ptr0
        else:
            # no sibling to compare with, this is the last node of linked list, move this node up
            # set ptr1 = ptr0, (as we move ptr1 up always (for simpler code))
            ptrprev.sibling = None
            ptr1 = ptr0
        
        # move ptr1 to linked list of nodes that have knocked their siblings
        num += 1
        if head == None:
            head = ptr1
            curr = head
        else:
            curr.sibling = ptr1
            curr = ptr1
        
        # move original lists' pointer to next set of nodes
        ptrprev = ptr0
        ptr0 = ptr0.sibling
    
    if num > 1:
        # not yet done, we need more tournaments
        return get_smallest(head)
    else:
        # done
        print "Smallest element =", head.val
        print "Total comparisons =", num_compare
        
        # print child list, nodes that smallest knocked off
        print "Nodes knocked off by the smallest =",
        print_child_list(head.child)
        print
        
        return head

def get_second_smallest(smallest):
    global num_compare
    
    # compute second smallest by traversing child nodes of smallest
    ptr = smallest.child
    if ptr == None:
        print "No second smallest element found"
        print "Total comparisons:", num_compare
    else:
        v = ptr.val
        while ptr.child != None:
            # increment num compare
            num_compare += 1
            
            ptr = ptr.child
            if ptr.val < v:
                v = ptr.val
                
        print "Second smallest =", v
        print "Total comparisons =", num_compare


arr = [2, 4, 3, 7, 3, 0, 8, 4, 11, 1]

# create linked list of input array
head = create_linked_list(arr)

# print linked list
print "Initial array =",
print_linked_list(head)
print

# compute smallest element
smallest = get_smallest(head)

# get the smallest
get_second_smallest(smallest)