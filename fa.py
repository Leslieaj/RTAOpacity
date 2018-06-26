#some definitions about finite automaton

from rta import *

class TimedLabel:
    def __init__(self, name="", label="", nfc = None):
        self.name = name
        self.label = label
        self.nfc = nfc
    def show(self):
        print self.name
        print self.label
        self.nfc.show()

    def __eq__(self, timedlabel):
        if self.label == timedlabel.label and nform_equal(self.nfc, timedlabel.nfc) == True:
            return True
        else:
            return False

class FATran:
    def __init__(self, id, source="", target="", timedlabel=None):
        self.id = id
        self.source = source
        self.target = target
        self.timedlabel = timedlabel

class FA:
    def __init__(self, name="", timed_alphabet = {}, states = None, trans = [], initstate_name = "", accept_names = []):
        self.name = name
        self.timed_alphabet = timed_alphabet
        self.states = states
        self.trans = trans
        self.initstate_name = initstate_name
        self.accept_names = accept_names
    def show(self):
        print self.name
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
        print self.initstate_name
        print self.accept_names    

class RFATran:
    def __init__(self, id, source="", target="", label="", nfnums = []):
        self.id = id
        self.source = source
        self.target = target
        self.label = label
        self.nfnums = nfnums

class RFA:
    def __init__(self, name="", timed_alphabet = {}, states = None, trans = [], initstate_name = "", accept_names = []):
        self.name = name
        self.timed_alphabet = timed_alphabet
        self.states = states
        self.trans = trans
        self.initstate_name = initstate_name
        self.accept_names = accept_names
    def show(self):
        print self.name
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
            print t.label, t.nfnums
            for nfnum in t.nfnums:
                self.timed_alphabet[t.label][nfnum].show()
                print
            print
        print self.initstate_name
        print self.accept_names    

def rta_to_fa(rta, flag):
    temp_alphabet = []
    trans = []
    for tran in rta.trans:
        label = copy.deepcopy(tran.label)
        nfc = copy.deepcopy(tran.nfc)
        timed_label = TimedLabel("",label,nfc)
        temp_alphabet += [timed_label]
        source = tran.source
        target = tran.target
        id = tran.id
        fa_tran = FATran(id, source, target, timed_label)
        trans.append(fa_tran)
    name = "FA_" + rta.name
    states = copy.deepcopy(rta.states)
    initstate_name = rta.initstate_name
    accept_names = []
    if flag == "generation": #means generation language
        for state in states:
            state.accept = True
            accept_names.append(state.name)
    elif flag == "receiving": #means receiving language
        accept_names = copy.deepcopy(rta.accept_names)
    else:
        accept_names = copy.deepcopy(rta.accept_names)
    timed_alphabet = alphabet_classify(temp_alphabet, rta.sigma)
    return FA(name, timed_alphabet, states, trans, initstate_name, accept_names)

def alphabet_classify(timed_alphabet, sigma):
    temp_set = {}
    for label in sigma:
        temp_set[label] = []
        for timedlabel in timed_alphabet:
            if timedlabel.label == label:
                temp_set[label].append(timedlabel)
    return temp_set

def alphabet_combine(alphabet1, alphabet2):
    combined_alphabet = {} 
    for key in alphabet1:
        combined_alphabet[key] = alphabet1[key] + alphabet2[key]
    return combined_alphabet

def alphabet_partitions(timed_alphabet):
    alphapartitions = {}
    for key in timed_alphabet:
        nfpatitions = []
        for timedlabel in timed_alphabet[key]:
            nfpatitions = nforms_partitions(nfpatitions, timedlabel.nfc)
        alphapartitions[key] = nfpatitions
    return alphapartitions

def fa_to_rfa(fa, alphapartitions):
    name = copy.deepcopy(fa.name)
    timed_alphabet = copy.deepcopy(alphapartitions)
    states = copy.deepcopy(fa.states)
    trans = []
    for tran in fa.trans:
        tran_id = tran.id
        source = tran.source
        target = tran.target
        label = tran.timedlabel.label
        nfnums = []
        for nf, i in zip(timed_alphabet[label], range(0, len(timed_alphabet[label]))):
            if nform_containedin(nf, tran.timedlabel.nfc) == True:
                nfnums.append(i)
        new_tran = RFATran(tran_id, source, target, label, nfnums)
        trans.append(new_tran)
    initstate_name = copy.deepcopy(fa.initstate_name)
    accept_names = copy.deepcopy(fa.accept_names)
    rfa = RFA(name, timed_alphabet, states, trans, initstate_name, accept_names)
    return rfa

def rfa_complement(rfa):
    name = "C_" + rfa.name
    states_num = len(rfa.states)
    states = copy.deepcopy(rfa.states)
    initstate_name = copy.deepcopy(rfa.initstate_name)
    accept_names = copy.deepcopy(rfa.accept_names)
    timed_alphabet = copy.deepcopy(rfa.timed_alphabet)
    new_state = State(str(states_num+1), False, True)
    states.append(new_state)
    accept_names.append(new_state.name)
    sigma = [term for term in rfa.timed_alphabet]
    trans = copy.deepcopy(rfa.trans)
    for s in states:
        nfnums_need = {}
        nfnums_exist = {}
        for term in sigma:
            nfnums_need[term] = []
            nfnums_exist[term] = []
        for rfatran in rfa.trans:
            if rfatran.source == s.name:
                for i in rfatran.nfnums:
                    if i not in nfnums_exist[rfatran.label]:
                        nfnums_exist[rfatran.label].append(i)
        for term in nfnums_exist:
            for i in range(0, len(timed_alphabet[term])):
                if i not in nfnums_exist[term]:
                    nfnums_need[term].append(i)
        for term in nfnums_need:
            if len(nfnums_need[term]) > 0:
                tran_id = len(trans)
                source = s.name
                target = new_state.name
                label = term
                nfnums = nfnums_need[term]
                new_tran = RFATran(tran_id, source, target, label, nfnums)
                trans.append(new_tran)
    if len(trans) == len(rfa.trans):
        states.remove(new_state)
        accept_names.remove(new_state.name)
    comp_rfa = RFA(name, timed_alphabet, states, trans, initstate_name, accept_names)
    return comp_rfa

def main():
    print("---------------------a.json----------------")
    A = buildRTA("a.json")
    A.show()
    print("-------------a_secret.json-----------------")
    AS = buildRTA("a_secret.json")
    AS.show()
    print("------------A to fa------------------------")
    A_FA = rta_to_fa(A, "generation")
    A_FA.show()
    print("-----------A_secret to FA-----------------------")
    AS_FA = rta_to_fa(AS, "receiving")
    AS_FA.show()
    print("---------------------partitions-------------")
    combined_alphabet = alphabet_combine(A_FA.timed_alphabet, AS_FA.timed_alphabet)
    alphapartitions = alphabet_partitions(combined_alphabet)
    #for key in alphapartitions:
        #print key
        #for nf in alphapartitions[key]:
            #nf.show()
            #print
    print("-------------------A to rfa--------------------")
    A_RFA = fa_to_rfa(A_FA, alphapartitions)
    A_RFA.show()
    print("-------------------A_secret to rfa--------------------")
    AS_RFA = fa_to_rfa(AS_FA, alphapartitions)
    AS_RFA.show()
    print("-------------------A_secret complement--------------------")
    C_AS_RFA = rfa_complement(AS_RFA)
    C_AS_RFA.show()

if __name__=='__main__':
	main()
