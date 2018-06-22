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
    m = lcm(X.k, Y.k)
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
            new_constraint = constraint + k_constraint
            new_x2.append(new_constraint)
    for i in range(m_l_1 + 1):
        l_constraint = Constraint('['+str(i * Y.k)+','+str(i * Y.k)+']')
        for constraint in Y.x2:
            new_constraint = constraint + l_constraint
            new_x2.append(new_constraint)
    new_x2 = unintersect_intervals(new_x2)
    return WNForm(new_x1, new_x2, m)
    
def nform_add(X, Y):
    #build wnform1: x1 = X.x1 + Y.x1, x2 = X.x1 + Y.x2, k = Y.k
    wnform1_x1 = []
    for c1 in X.x1:
        for c2 in Y.x1:
            temp = c1 + c2
            #print temp.show()
            if temp.isEmpty() == False:
                wnform1_x1.append(temp)
    wnform1_x1 = unintersect_intervals(wnform1_x1)
    wnform1_x2 = []
    for c1 in X.x1:
        for c2 in Y.x2:
            temp = c1 + c2
            #print temp.show()
            if temp.isEmpty() == False:
                wnform1_x2.append(temp)
    wnform1_x2 = unintersect_intervals(wnform1_x2)
    wnform1_k = Y.k
    wnform1 = WNForm(wnform1_x1, wnform1_x2, wnform1_k)
    #build wnform2: x1 = [], x2 = X.x2 + Y.x1, k = X.k
    wnform2_x1 = []
    wnform2_x2 = []
    for c1 in X.x2:
        for c2 in Y.x1:
            temp = c1 + c2
            if temp.isEmpty() == False:
                wnform2_x2.append(temp)
    wnform2_x2 = unintersect_intervals(wnform2_x2)
    wnform2_k = X.k
    wnform2 = WNForm(wnform2_x1, wnform2_x2, wnform2_k)
    #build wnform3: x1 = [], x2 = X.x2 + Y.x2, k = {X.k}* + {Y.k}*
    #then we transform it to: x1 = X.x2 + Y.x2 + B, x2 = X.x2 + Y.x2 + {lcm(X.k, Y.k)}, k = gcd(X.k, Y.k)
    #where B = {a \in Q| 0<=a<lcm(X.k, Y.k), a = l*X.k + m*Y.k, l,m \in N}
    B, B_dot = calculate_B(X.k, Y.k)
    wnform3_x1 = []
    for c1 in X.x2:
        for c2 in Y.x2:
            for c3 in B:
                temp1 = c1 + c2
                temp2 = temp1 + c3
                if temp2.isEmpty() == False:
                    wnform3_x1.append(temp2)
    wnform3_x1 = unintersect_intervals(wnform3_x1)
    ceil = lcm(X.k, Y.k)
    lcm_constraint = Constraint('['+str(ceil)+','+str(ceil)+']')
    wnform3_x2 = []
    for c1 in X.x2:
        for c2 in Y.x2:
            temp1 = c1 + c2
            temp2 = temp1 + lcm_constraint
            if temp2.isEmpty() == False:
                wnform3_x2.append(temp2)
    wnform3_x2 = unintersect_intervals(wnform3_x2)
    wnform3_k = gcd(X.k, Y.k)
    wnform3 = WNForm(wnform3_x1, wnform3_x2, wnform3_k)
    return wnform1, wnform2, wnform3

def calculate_B(p, q):
    #B = {a \in Q| 0<=a<lcm(p, q), a = l*p + m*q, l,m \in N}
    ceil = lcm(p,q)
    l = 0
    m = 0
    B_dot = []
    while l*p < ceil:
        l = l + 1
    while m*q < ceil:
        m = m + 1
    for i in range(0, l+1):
        for j in range(0, m+1):
            if i*p + j*q < ceil:
                a= i*p + j*q
                #print a
                if a not in B_dot:
                    B_dot.append(a)
    B_dot.sort()
    B = []
    for a in B_dot:
        new_constraint = Constraint('['+str(a)+','+str(a)+']')
        B.append(new_constraint)
    return B, B_dot

def main():
    c1 = Constraint("[3,5]")
    c2 = Constraint("[6,7]")
    c3 = Constraint("[3,5]")
    c4 = Constraint("[0,1)")
    c5 = Constraint("(8,+)")
    l1 = [c2,c1,c5,c4,c3]
    
    c6 = Constraint("[2,2]")
    c7 = Constraint("[3,4]")
    c8 = Constraint("(5,7]")
    c9 = Constraint("[12,+)")
    l2 = [c7,c9,c6,c8]
    
    print("------------------nf1--------------------")
    nf1 = union_intervals_to_nform(l1)
    print "x1: "
    for c in nf1.x1:
        print c.show()
    print "x2: "
    for c in nf1.x2:
        print c.show()
    print "k, N: "
    print nf1.k, nf1.N
    print("------------------nf2--------------------")
    nf2 = union_intervals_to_nform(l2)
    print "x1: "
    for c in nf2.x1:
        print c.show()
    print "x2: "
    for c in nf2.x2:
        print c.show()
    print "k, N: "
    print nf2.k, nf2.N
    print("-------------nf1 U nf2-------------------")
    u_nf1_2 = nform_union(nf1, nf2)
    print "x1: "
    for c in u_nf1_2.x1:
        print c.show()
    print "x2: "
    for c in u_nf1_2.x2:
        print c.show()
    print "k: "
    print u_nf1_2.k
    print("--------------calculate_B----------------")
    p = 1
    q = 1
    B, B_dot = calculate_B(p,q)
    for c in B:
        print c.show()
    print B_dot
    print("--------------nf1 + nf2------------------")
    wnform1,wnform2,wnform3 = nform_add(nf1,nf2)
    print("--------------wnform1--------------------")
    print "x1: "
    for c in wnform1.x1:
        print c.show()
    print "x2: "
    for c in wnform1.x2:
        print c.show()
    print "k: "
    print wnform1.k
    print("--------------wnform2--------------------")
    print "x1: "
    for c in wnform2.x1:
        print c.show()
    print "x2: "
    for c in wnform2.x2:
        print c.show()
    print "k: "
    print wnform2.k
    print("--------------wnform3--------------------")
    print "x1: "
    for c in wnform3.x1:
        print c.show()
    print "x2: "
    for c in wnform3.x2:
        print c.show()
    print "k: "
    print wnform3.k

if __name__=='__main__':
	main()
