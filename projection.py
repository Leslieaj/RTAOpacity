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
    print("-------------------BTau------------------------------")
    observable = ['a']
    Btau = buildBTau(A_FA, observable)
    Btau.show()

if __name__=='__main__':
	main()   
