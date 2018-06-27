#define B_tau and some functions about projection

from fa import *

class BTau:
    def __init__(self, states = [], timed_alphabet = {}, trans = [], initstates = [], accept_names = []):
        self.states = states
        self.timed_alphabet = timed_alphabet
        self.trans = trans
        self.initstates = initstates
        self.accept_names = accept_names
    def show(self):
        for term in self.timed_alphabet:
            print term
            print
            for timedlabel in self.timed_alphabet[term]:
                timedlabel.show()
                print
        for s in self.states:
            print s.name, s.init, s.accept
        for t in self.trans:
            print t.id, t.source, t.target
            t.timedlabel.show()
            print
        print self.initstates
        print self.accept_names

def isinBTalphabet(nf, timed_alphabet):
    for nfpartition in timed_alphabet["Tau"]:
        if nform_equal(nf, nfpartition) == True:
            return True
    return False

def buildBTau(fa, observable):
    states = copy.deepcopy(fa.states)
    trans = []
    temp_alphabet = {}
    temp_alphabet["Tau"] = []
    initstate_name = [fa.initstate_name]
    accept_names = copy.deepcopy(fa.accept_names)
    for tran in fa.trans:
        if tran.timedlabel.label not in observable:
            index = len(trans)
            new_timedlabel = TimedLabel("Tau"+str(len(temp_alphabet["Tau"])), "Tau", tran.timedlabel.nfc)
            new_tran = FATran(index, tran.source, tran.target, new_timedlabel)
            trans.append(new_tran)
            if isinBTalphabet(tran.timedlabel.nfc, temp_alphabet) == False:
                temp_alphabet["Tau"].append(tran.timedlabel.nfc)
        else:
            if tran.target not in initstate_name:
                initstate_name.append(tran.target)
            if tran.source not in accept_names:
                accept_names.append(tran.source)
    for s in states:
        s.init = False
        s.accept = False
        if s.name in initstate_name:
            s.init = True
        if s.name in accept_names:
            s.accept = True
    return BTau(states, temp_alphabet, trans, initstate_name, accept_names)

def unobservable_intervals(btau):
    n = len(btau.states)
    empty_nf = NForm([],[],1,1)
    zero_nf = NForm([Constraint("[0,0]")],[],1,1)
    RE = [[empty_nf for col in range(n)] for row in range(n)]
    for s_i, i in zip(btau.states, range(0,n)):
        for s_j, j in zip(btau.states, range(0,n)):
            temp_source = s_i.name
            temp_target = s_j.name
            for tran in btau.trans:
                if temp_source == tran.source and temp_target == tran.target:
                    RE[i][j] = nform_union(RE[i][j], tran.timedlabel.nfc)
    for i in range(0,n):
        RE[i][i] = nform_union(RE[i][i], zero_nf)
    RE_new = copy.deepcopy(RE)
    for k in range(0, n):
        for i in range(0, n):
            for j in range(0, n):
                RE_new[i][j] = nform_union(RE[i][j], nform_add(nform_add(RE[i][k], nform_star(RE[k][k])), RE[k][j]))
        RE = copy.deepcopy(RE_new)
    return RE

def delete_unobservable_trans(fa, observable):
    new_fa = copy.deepcopy(fa)
    obser_trans = []
    for tran in new_fa.trans:
        if tran.timedlabel.label in observable:
            tran.id = len(obser_trans)
            obser_trans.append(tran)
    new_fa.trans = obser_trans
    return new_fa

def unobservable_trans(btau, RE):
    unobser_trans = []
    n = len(btau.states)
    for i in range(0, n):
        for j in range(0, n):
            if btau.states[i].init == True and btau.states[j].accept == True:
                if RE[i][j].isEmpty() == False and nform_equal(RE[i][j], NForm([Constraint("[0,0]")],[],1,1)) == False: 
                #RE[i][j] is not empty normalform and zero normalform
                    source_state = btau.states[i].name
                    target_state = btau.states[j].name
                    new_timedlabel = TimedLabel("", "Tau", RE[i][j])
                    new_tran = FATran(len(unobser_trans), source_state, target_state, new_timedlabel)
                    unobser_trans.append(new_tran)
    return unobser_trans

def new_observable_trans(fa, unobser_trans):
    new_trans = []
    new_trans.extend(fa.trans)
    for ut in unobser_trans:
        new_source = ut.target
        for tran in fa.trans:
            if tran.source == new_source:
                new_target = tran.target
                new_nfc = nform_add(ut.timedlabel.nfc, tran.timedlabel.nfc)
                new_timedlabel = TimedLabel("", tran.timedlabel.label, new_nfc)
                new_tran = FATran(len(new_trans), ut.source, tran.target, new_timedlabel)
                new_trans.append(new_tran)
    return new_trans

def projection(fa, observable):
    btau = buildBTau(fa, observable)
    RE = unobservable_intervals(btau)
    new_fa = delete_unobservable_trans(fa, observable)
    unobser_trans = unobservable_trans(btau, RE)
    new_trans = new_observable_trans(new_fa, unobser_trans)
    trans = []
    trans.extend(new_trans)
    temp_alphabet = []
    sigma = []
    state_names = []
    accept_names = []
    for tran in trans:
        label = tran.timedlabel.label
        if label not in sigma:
           sigma.append(label)
        if tran.timedlabel not in temp_alphabet:
            temp_alphabet.append(tran.timedlabel)
        if tran.source not in state_names:
            state_names.append(tran.source)
        if tran.target not in state_names:
            state_names.append(tran.target)
    new_states = []
    for s in new_fa.states:
        if s.name in state_names:
            new_states.append(s)
            if s.accept == True:
                accept_names.append(s.name)
    name = "projection_" + new_fa.name
    initstate_name = new_fa.initstate_name
    timed_alphabet = alphabet_classify(temp_alphabet,sigma)
    projection_fa = FA(name, timed_alphabet, new_states, trans, initstate_name, accept_names)
    return projection_fa

def main():
    print("---------------------a.json----------------")
    A = buildRTA("a.json")
    #A.show()
    print("-------------a_secret.json-----------------")
    AS = buildRTA("a_secret.json")
    #AS.show()
    print("------------B : A to fa------------------------")
    A_FA = rta_to_fa(A, "generation")
    A_FA.show()
    print("-----------A_secret to FA-----------------------")
    AS_FA = rta_to_fa(AS, "receiving")
    #AS_FA.show()
    print("---------------------partitions-------------")
    combined_alphabet = alphabet_combine(A_FA.timed_alphabet, AS_FA.timed_alphabet)
    alphapartitions = alphabet_partitions(combined_alphabet)
    #for key in alphapartitions:
        #print key
        #for nf in alphapartitions[key]:
            #nf.show()
            #print
    print("-------------------B': A to rfa--------------------")
    A_RFA = fa_to_rfa(A_FA, alphapartitions)
    #A_RFA.show()
    print("-------------------B_secret: A_secret to rfa--------------------")
    AS_RFA = fa_to_rfa(AS_FA, alphapartitions)
    #AS_RFA.show()
    print("-------------------B_secret_comp: B_secret complement--------------------")
    C_AS_RFA = rfa_complement(AS_RFA)
    #C_AS_RFA.show()
    print("-------------------B' x B_secret_comp----------------------")
    P_A_AS = rfa_product(A_RFA, C_AS_RFA)
    #P_A_AS.show()
    print("-------------------clean rfa-----------------------")
    clean_P_A_AS = clean_deadstates(P_A_AS)
    #clean_P_A_AS.show()
    print("-------------------Bns: rfa to fa----------------------")
    Bns_FA = rfa_to_fa(clean_P_A_AS)
    #Bns_FA.show()
    print("-------------------B_Tau------------------------------")
    observable = ['a']
    B_tau = buildBTau(A_FA, observable)
    B_tau.show()
    print("-------------------Bns_Tau------------------------------")
    Bns_tau = buildBTau(Bns_FA, observable)
    Bns_tau.show()
    #print("-------------------B_Tau unobservable_intervals------------------------------")
    #RE = unobservable_intervals(B_tau)
    #n = len(Btau.states)
    #for i in range(0,n):
        #for j in range(0,n):
            #RE[i][j].show()
            #print
    print("---------------------projection B------------------------")
    projection_B = projection(A_FA, observable)
    projection_B.show()
    print("---------------------projection Bns------------------------")
    projection_Bns = projection(Bns_FA, observable)
    projection_Bns.show()
    print("---------------------projection_B_RFA: fa to rfa")
    combined_alphabet1 = alphabet_combine(projection_B.timed_alphabet, projection_Bns.timed_alphabet)
    alphapartitions1 = alphabet_partitions(combined_alphabet1)
    PROJ_B_RFA = fa_to_rfa(projection_B, alphapartitions1)
    PROJ_Bns_RFA = fa_to_rfa(projection_Bns, alphapartitions1)
    #PROJ_B_RFA.show()
    print("----------------------PROJ_B_RFA: nfa to dfa--------------------")
    PROJ_B_RFA_D = nfa_to_dfa(PROJ_B_RFA)
    #PROJ_B_RFA_D.show()
    print("----------------------PROJ_Bns_RFA: nfa to dfa--------------------")
    PROJ_Bns_RFA_D = nfa_to_dfa(PROJ_Bns_RFA)
    #PROJ_Bns_RFA_D.show()
    print("----------------------PROJ_Bns_RFA complement-------------------------")
    C_PROJ_Bns_RFA_D = rfa_complement(PROJ_Bns_RFA_D)
    #C_PROJ_Bns_RFA_D.show()
    print("----------------------PROJ_B_RFA X C_PROJ_Bns_RFA-------------------------")
    product_final = rfa_product(PROJ_B_RFA_D, C_PROJ_Bns_RFA_D)
    product_final.show()

if __name__=='__main__':
	main()   
