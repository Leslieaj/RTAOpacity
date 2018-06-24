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
            for timedlabel in self.timed_alphabet[term]:
                timedlabel.show()
        for s in self.states:
            print s.name, s.init, s.accept
        for t in self.trans:
            print t.id, t.source, t.target
            t.timedlabel.show()
            print
        print self.initstate_name
        print self.accept_names    

def rta_to_fa(rta):
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
    for state in states:
        state.accept = True
        accept_names.append(state.name)
    timed_alphabet = alphabet_classify(temp_alphabet, rta.sigma)
    return FA(name, timed_alphabet, states, trans, initstate_name, accept_names)

def alphabet_classify(timed_alphabet, sigma):
    temp_set = {}
    for label in sigma:
        temp_set[label] = []
        #label_list = []
        for timedlabel in timed_alphabet:
            if timedlabel.label == label:
                temp_set[label].append(timedlabel)
    return temp_set

def main():
    print("---------------------a.json----------------")
    A = buildRTA("a.json")
    A.show()
    print("-------------a_secret.json-----------------")
    AS = buildRTA("a_secret.json")
    AS.show()
    print("------------A to fa------------------------")
    A_FA = rta_to_fa(A)
    A_FA.show()
    print("-----------A_secret to FA-----------------------")
    AS_FA = rta_to_fa(AS)
    AS_FA.show()

if __name__=='__main__':
	main()
