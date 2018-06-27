# The main procedure of deciding the language opacity of RTA

import sys
from projection import *

def language_opacity(A, AS, observable):
    #print("------------B : A to fa------------------------")
    A_FA = rta_to_fa(A, "generation")
    #print("-----------A_secret to FA-----------------------")
    AS_FA = rta_to_fa(AS, "receiving")
    #print("---------------------partitions-------------")
    combined_alphabet = alphabet_combine(A_FA.timed_alphabet, AS_FA.timed_alphabet)
    alphapartitions = alphabet_partitions(combined_alphabet)
    #print("-------------------B': A to rfa--------------------")
    A_RFA = fa_to_rfa(A_FA, alphapartitions)
    #print("-------------------B_secret: A_secret to rfa--------------------")
    AS_RFA = fa_to_rfa(AS_FA, alphapartitions)
    #print("-------------------B_secret_comp: B_secret complement--------------------")
    C_AS_RFA = rfa_complement(AS_RFA)
    #print("-------------------B' x B_secret_comp----------------------")
    P_A_AS = rfa_product(A_RFA, C_AS_RFA)
    #print("-------------------clean rfa-----------------------")
    clean_P_A_AS = clean_deadstates(P_A_AS)
    #print("-------------------Bns: rfa to fa----------------------")
    Bns_FA = rfa_to_fa(clean_P_A_AS)
    #print("-------------------B_Tau------------------------------")
    B_tau = buildBTau(A_FA, observable)
    #print("-------------------Bns_Tau------------------------------")
    Bns_tau = buildBTau(Bns_FA, observable)
    #print("---------------------projection B------------------------")
    projection_B = projection(A_FA, observable)
    #print("---------------------projection Bns------------------------")
    projection_Bns = projection(Bns_FA, observable)
    #print("---------------------projection_B_RFA: fa to rfa")
    combined_alphabet1 = alphabet_combine(projection_B.timed_alphabet, projection_Bns.timed_alphabet)
    alphapartitions1 = alphabet_partitions(combined_alphabet1)
    PROJ_B_RFA = fa_to_rfa(projection_B, alphapartitions1)
    PROJ_Bns_RFA = fa_to_rfa(projection_Bns, alphapartitions1)
    #print("----------------------PROJ_B_RFA: nfa to dfa--------------------")
    PROJ_B_RFA_D = nfa_to_dfa(PROJ_B_RFA)
    #print("----------------------PROJ_Bns_RFA: nfa to dfa--------------------")
    PROJ_Bns_RFA_D = nfa_to_dfa(PROJ_Bns_RFA)
    #print("----------------------PROJ_Bns_RFA complement-------------------------")
    C_PROJ_Bns_RFA_D = rfa_complement(PROJ_Bns_RFA_D)
    print("----------------------final FA-------------------------")
    product_final = rfa_product(PROJ_B_RFA_D, C_PROJ_Bns_RFA_D)
    product_final.show()
    #print "Total time: ", end - start
    print("-----------------------cleaned final FA---------------------------")
    cleaned_product_final = clean_deadstates(product_final)
    cleaned_product_final.show()
    
    if len(cleaned_product_final.accept_names) == 0:
        return True
    else:
        return False

def main():
    para = sys.argv
    file1 = str(para[1])
    file2 = str(para[2])
    print("---------------------" + file1 + "----------------")
    A, observable = buildRTA(file1)
    A.show()
    print("-------------" + file2 + "-----------------")
    AS, _ = buildRTA(file2)
    AS.show()
    start = time.time()
    language_opaque = language_opacity(A, AS, observable)
    end = time.time()
    print
    print("*************************")
    if language_opaque == True:
        print "Language Opaque!"
    else:
        print "NOT!"
    print("*************************")
    print
    print "Total time: ", end - start

if __name__=='__main__':
	main()  
