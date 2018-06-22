#some defines about intervals

import copy
from enum import IntEnum

global MAXVALUE
MAXVALUE = 10000

class Bracket(IntEnum):
    """
    Left Open, Left Closed, Right Open, Right Closed.
    """
    RO = 1
    LC = 2
    RC = 3
    LO = 4

class BracketNum:
    def __init__(self, value="", bracket=0):
        self.value = value
        self.bracket = bracket
    def __eq__(self, bn):
        if self.value == bn.value and self.bracket == bn.bracket:
            return True
        else:
            return False
    def __lt__(self, bn):
        if self.value == '+':
            return False
        if bn.value == '+':
            return True
        if int(self.value) > int(bn.value):
            return False
        elif int(self.value) < int(bn.value):
            return True
        else:
            if self.bracket < bn.bracket:
                return True
            else:
                return False
    def __gt__(self, bn):
        if self.value == '+':
            if bn.value == '+':
                return False
            else:
                return True
        if int(self.value) > int(bn.value):
            return True
        elif int(self.value) < int(bn.value):
            return False
        else:
            if self.bracket > bn.bracket:
                return True
            else:
                return False
    def __ge__(self, bn):
        return not self.__lt__(bn)
    def __le__(self, bn):
        return not self.__gt__(bn)
    def complement(self):
        if self.value == '+':
            return BracketNum('+', Bracket.RO)  #ceil
        if self.value == '0' and self.bracket == Bracket.LC:
            return BracketNum('0', Bracket.LC)  #floor
        temp_value = self.value
        temp_bracket = None
        if self.bracket == Bracket.LC:
            temp_bracket = Bracket.RO
        if self.bracket == Bracket.RC:
            temp_bracket = Bracket.LO
        if self.bracket == Bracket.LO:
            temp_bracket = Bracket.RC
        if self.bracket == Bracket.RO:
            temp_bracket = Bracket.LC
        return BracketNum(temp_value, temp_bracket)
    
    def getbn(self):
        if self.bracket == Bracket.LC:
            return '[' + self.value
        if self.bracket == Bracket.LO:
            return '(' + self.value
        if self.bracket == Bracket.RC:
            return self.value + ']'
        if self.bracket == Bracket.RO:
            return self.value + ')'

class Constraint:
    guard=None
    min_value = ""
    closed_min = True
    max_value = ""
    closed_max = True
    min_bn = None
    max_bn = None
    def __init__(self, guard=None):
        self.guard = guard
        self.__build()
    
    def __build(self):
        min_type, max_type = self.guard.split(',')
        min_bn_bracket = None
        max_bn_bracket = None
        if min_type[0] == '[':
            self.closed_min = True
            min_bn_bracket = Bracket.LC
        else:
            self.closed_min = False
            min_bn_bracket = Bracket.LO
        self.min_value = min_type[1:].strip()
        self.min_bn = BracketNum(self.min_value, min_bn_bracket)
        if max_type[-1] == ']':
            self.closed_max = True
            max_bn_bracket = Bracket.RC
        else:
            self.closed_max = False
            max_bn_bracket = Bracket.RO
        self.max_value = max_type[:-1].strip()
        self.max_bn = BracketNum(self.max_value, max_bn_bracket)
    
    def __eq__(self, constraint):
        if self.min_value == constraint.min_value and self.closed_min == constraint.closed_min and self.max_value == constraint.max_value and self.closed_max == constraint.closed_max:
            return True
        else:
            return False

    def __add__(self, constraint):
        if self.isEmpty() == True or constraint.isEmpty() == True:
            return Constraint("(0,0)")
        else:
            temp_min_value = ""
            temp_max_value = ""
            if self.min_value == '+' or constraint.min_value == '+':
                temp_min_value = '+'
            else:
                temp_min_value = str(int(self.min_value) + int(constraint.min_value))
            if self.max_value == '+' or constraint.max_value == '+':
                temp_max_value = '+'
            else:
                temp_max_value = str(int(self.max_value) + int(constraint.max_value))
            temp_closed_min = '('
            temp_closed_max = ')'
            if self.closed_min == True and constraint.closed_min == True:
                temp_closed_min = '['
            if self.closed_max == True and constraint.closed_max == True:
                temp_closed_max = ']'
            guard = temp_closed_min + temp_min_value + ',' + temp_max_value + temp_closed_max
            return Constraint(guard)

    def isEmpty(self):
        if self.max_bn < self.min_bn:
            return True
        else:
            return False
    
    def isininterval(self, num):
        if self.max_value == '+':
            return True
        if num < self.get_min():
            return False
        elif num == self.get_min():
            if self.closed_min == True:
                return True
            else:
                return False
        elif num > self.get_min() and num < self.get_max():
            return True
        elif num == self.get_max():
            if self.closed_max == True:
                return True
            else:
                return False
        else:
            return False

    def get_min(self):
        return int(self.min_value)
    
    def get_max(self):
        if self.max_value == '+':
            closed_max=False
            return MAXVALUE
        else:
            return int(self.max_value)
    
    def show(self):
        return self.guard

def intersect_constraint(c1, c2):
    min_bn1 = c1.min_bn
    max_bn1 = c1.max_bn
    min_bn2 = c2.min_bn
    max_bn2 = c2.max_bn
    bnlist = [min_bn1, max_bn1, min_bn2, max_bn2]
    bnlist.sort()
    left_bn = bnlist[1]
    right_bn = bnlist[2]
    if left_bn in [min_bn1, min_bn2] and right_bn in [max_bn1, max_bn2]:
        return Constraint(left_bn.getbn()+','+right_bn.getbn()), True
    else:
        return Constraint("(0,0)"), False

def union_constraint(c1, c2):
    sortlist = [c1,c2]
    lqsort(sortlist, 0, len(sortlist)-1)
    if int(sortlist[1].min_bn.value) < int(sortlist[0].max_bn.value):
        temp_bn = sortlist[0].max_bn
        if sortlist[0].max_bn < sortlist[1].max_bn:
            temp_bn = sortlist[1].max_bn
        return Constraint(sortlist[0].min_bn.getbn()+','+temp_bn.getbn()), 1
    elif int(sortlist[1].min_bn.value) == int(sortlist[0].max_bn.value):
        if sortlist[0].max_bn.bracket == Bracket.RO and sortlist[1].min_bn.bracket == Bracket.LO:
            return sortlist, 2
        else:
            return Constraint(sortlist[0].min_bn.getbn()+','+sortlist[1].max_bn.getbn()), 1
    else:
        return sortlist, 2

def intervals_partition(intervals):
    partitions = []
    floor_bn = BracketNum('0',Bracket.LC)
    ceil_bn = BracketNum('+',Bracket.RO)
    key_bns = []
    for constraint in intervals:
        min_bn = constraint.min_bn
        max_bn = constraint.max_bn
        if min_bn not in key_bns:
            key_bns+= [min_bn]
        if max_bn not in key_bns:
            key_bns+=[max_bn]
    key_bnsc = copy.deepcopy(key_bns)
    for bn in key_bns:
        bnc = bn.complement()
        if bnc not in key_bnsc:
            key_bnsc.append(bnc)
    if floor_bn not in key_bnsc:
        key_bnsc.append(floor_bn)
    if ceil_bn not in key_bnsc:
        key_bnsc.append(ceil_bn)
    key_bnsc.sort()
    for index in range(len(key_bnsc)):
        if index%2 == 0:
            temp_constraint = Constraint(key_bnsc[index].getbn()+','+key_bnsc[index+1].getbn())
            partitions.append(temp_constraint)
    return partitions, key_bnsc

def lqsort(array, left, right):
    if left < right:
        mid = lqsortpartition(array, left, right)
        lqsort(array, left, mid-1)
        lqsort(array, mid+1, right)

def lqsortpartition(array, left, right):
    temp = array[left]
    while left < right:
        while left < right and array[right].min_bn >= temp.min_bn:
            right = right - 1
        array[left] = array[right]
        while left < right and array[right].min_bn <= temp.min_bn:
            left = left + 1
        array[right] = array[left]
    array[left] = temp
    return left
 
def main():
    c1 = Constraint("(2,5)")
    c2 = Constraint("[2,6)")
    c3 = Constraint("[6,7)")
    c4 = Constraint("[7,9]")
    c5 = Constraint("[8,+)")
    b1 = BracketNum('6', Bracket.LO)
    b2 = BracketNum('6', Bracket.LC)
    b3 = BracketNum('+', Bracket.RO)
    b4 = BracketNum('7', Bracket.LC)
    b5 = BracketNum('6', Bracket.LO)
    uc,flag = union_constraint(c5,c4)
    if flag == 1:
        print uc.show(), flag
    else:
        for c in uc:
            print c.show()
        print flag
    l = [c2,c1,c5,c4,c3]
    lqsort(l, 0, 4)
    #partitions,_ = intervals_partition()
    for c in l:
        print c.show()

if __name__=='__main__':
	main()
