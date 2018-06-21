#some defines about intervals


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

def main():
    c1 = Constraint("[2,3]")
    c2 = Constraint("[2,3]")
    c3 = Constraint("(0,1]")
    c4 = Constraint("(0,0)")
    print c4.isEmpty()
    c5 = c1 + c3
    c6 = c1 + c4
    print c5.show()
    print c6.show()
    c7, isinter = intersect_constraint(c2,c3)
    print c7.show(), isinter

if __name__=='__main__':
	main()
