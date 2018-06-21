#some defines about normal form of the union of unintersect intervals
# depended on Dima's paper "Real-time Automaton"

from interval import *

class NForm:
    def __init__(self, x1, x2, k, N):
        self.x1 = x1
        self.x2 = x2
        self.k = k
        self.N = N

class WNForm:
    def __init__(self, x1, x2, k):
        self.x1 = x1
        self.x2 = x2
        self.k = k

def gcd(a, b):  
    #assert a > 0 and b > 0,'parameters must be greater than 0.'     
    while True:  
        if a >= b:  
            if a % b == 0:  
                return b  
            else:  
                a, b = a - b, b  
        else:  
            a, b = b, a  
  
def lcm(a, b):  
    #assert a > 0 and b > 0,'parameters must be greater than 0.'  
    return int(a * b / gcd(a, b))

def union_intervals_to_nform(uintervals):
    if len(uintervals) >= 1:
        x1 = unintersect_intervals(uintervals)
        k = 1
        constraint = x1[len(x1)-1]
        N = None
        x2 = []
        if constraint.max_value == '+':
            N = int(constraint.min_value)+1
            left,_ = constraint.guard.split(',')
            right = str(N) + ')'
            new_constraint = Constraint(left+','+right)
            x1 = x1[:-1]
            x1.append(new_constraint)
            x2.append(Constraint('['+str(N)+','+str(N+1)+')'))
        else:
            N = int(constraint.max_value)+1
        return NForm(x1,x2,k,N)

def nform_union(X, Y):
    m = lcm(X.k, Y.K)
    new_x1 = []
    new_x1.extend(X.x1)
    new_x1.extend(Y.x1)
    new_x1 = unintersect_intervals(new_x1)
    m_k_1 = m/X.k - 1
    m_l_1 = m/Y.k - 1
    new_x2 = []
    for i in range(m_k_1 + 1):
        k_constraint = Constraint('['+str(i * X.k)+','+str(i * X.k)+']')
        for constraint in X.x2:
            new_constraint = add_constraints(constraint, k_constraint)
            new_x2.append(new_constraint)
    for i in range(m_l_1 + 1):
        l_constraint = Constraint('['+str(i * Y.k)+','+str(i * Y.k)+']')
        for constraint in Y.x2:
            new_constraint = add_constraints(constraint, l_constraint)
            new_x2.append(new_constraint)
    new_x2 = unintersect_intervals(new_x2)
    return WNForm(new_x1, new_x2, m)

