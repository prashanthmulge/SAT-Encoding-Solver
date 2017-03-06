import math
import copy
from copy import deepcopy

file_read = open('input6', 'r')
file_write = open('output.txt', 'w')

player = file_read.readline().strip().split()
guest = int(player[0])
table = int(player[1])
main_model = set([])
main_symbols = set([])
cnfList = []


def cnfModeling(per1, per2, rel):
    print per1, per2, rel
    j = 1
    if rel == "F":
        while j <= table:
            subList = []
            subList.append("~X" + str(per1) + str(j))
            subList.append("X" + str(per2) + str(j))
            # symbols.add("~X" + str(relation[0]) + str(j))
            main_symbols.add("X" + str(per2) + str(j))
            cnfList.append(subList)
            # string = "~X" + str(relation[0]) + str(j) + "V" + "X" + str(relation[2]) + str(j)
            # cnfList.append(string)

            subList = []
            subList.append("X" + str(per1) + str(j))
            subList.append("~X" + str(per2) + str(j))
            main_symbols.add("X" + str(per1) + str(j))
            # symbols.add("~X" + str(relation[2]) + str(j))
            cnfList.append(subList)
            # string = "X" + str(relation[0]) + str(j) + "V" + "~X" + str(relation[2]) + str(j)
            # cnfList.append(string)
            j += 1
    else:
        while j <= table:
            subList = []
            subList.append("~X" + str(per1) + str(j))
            subList.append("~X" + str(per2) + str(j))
            main_symbols.add("X" + str(per1) + str(j))
            main_symbols.add("X" + str(per2) + str(j))
            # string = "~X" + str(relation[0]) + str(j) + "V" + "~X" + str(relation[2]) + str(j)
            # cnfList.append(string)
            cnfList.append(subList)
            j += 1


def guestOneTable():
    i = 1
    while i <= guest:
        j = 1
        string1 = ""
        string2 = ""
        subList1 = []
        subList2 = []

        while j <= table:
            subList1.append("X" + str(i) + str(j))
            main_symbols.add("X" + str(i) + str(j))
            # string1 += "X" + str(i) + str(j)
            subList2.append("~X" + str(i) + str(j))
            # if table > 1:
            #     symbols.add("~X" + str(i) + str(j))
            # string2 += "~X" + str(i) + str(j)
            # if j < table:
            #     # string1 += "V"
            #     # string2 += "V"
            #     subList1.append("V")
            #     subList2.append("V")

            j += 1
        cnfList.append(subList1)
        if table > 1:
            cnfList.append(subList2)
        i += 1


def findPureSymbol(clauses, symbols, model):
    print "Pure"
    toRemove = []
    if not symbols:
        return None
    isPure = 0
    for clause_ele in clauses:
        isPure = 1
        for del_clause in clause_ele:
            for ele in clauses:
                if del_clause[0] == "~":
                    if del_clause[1:] in ele:
                        isPure = 0
                        break
                else:
                    if ("~" + del_clause ) in ele:
                        isPure = 0
                        break
            if isPure:
                for j in clauses:
                    if del_clause in j:
                        toRemove.append(j)
                for ele in toRemove:
                    clauses.remove(ele)
                return del_clause
    return None




def findUnitClause(clauses, model):
    print "Unit"#, clauses
    toRemove = []
    for clause_ele in clauses:
        if len(clause_ele) == 1:

            for del_clause in clauses:
                if clause_ele[0] in del_clause:
                    toRemove.append(del_clause)
                else:
                    if clause_ele[0][0] == "~":
                        if clause_ele[0][1:] in del_clause:
                            del_clause.remove(clause_ele[0][1:])
                    else:
                        if ("~" + clause_ele[0]) in del_clause:
                            del_clause.remove("~" + clause_ele[0])
            for ele in toRemove:
                clauses.remove(ele)
            return clause_ele[0]
    return None


def checkForTrueClause(clause, newModel):
    if not newModel:
        return "Cont"
    toRemove = []
    for mod_ele in newModel:
        for clause_ele in clause:
            if not clause_ele:
                return False
            if mod_ele in clause_ele:
                toRemove.append(clause_ele)
                #clause.remove(clause_ele)
            else:
                if mod_ele[0] == "~":
                    if mod_ele[1:] in clause_ele:
                        clause_ele.remove(mod_ele[1:])
                else:
                    if ("~" + mod_ele) in clause_ele:
                        clause_ele.remove("~" + mod_ele)
                if not clause_ele:
                    return False

    if not clause:
        print "One of the output is ", newModel
        return True

    for c in clause:
        if not c:
            return False

    for ele in toRemove:
        clause.remove(ele)
    return "Cont"


def model_union(new_model, pop_str, type):
    if type == 1:
        new_model.add(pop_str)
    else:
        new_model.add("~" + pop_str)

    return deepcopy(new_model)


def removeSymbol(new_symbol, str1):
    if str1[0] == "~":
        new_symbol.discard(str1[1:])
    else:
        new_symbol.discard(str1)


def dpllImplementation(clause, symbols, model):
    print "In DPLL"
    # print "In DPLL Clause : " , clause
    if not clause:
        print "One of the output is ", model
        return True
    ret = checkForTrueClause(clause, model)

    if ret == True:
        print "One of the output is ", model
        return True
    elif ret == False:
        return False
    else:
        print "Clause ", clause
        P = findPureSymbol(clause, symbols, model)
        if P:

            model.add(str(P))
            if symbols:
                removeSymbol(symbols, P)
            print "Pure Symbol : " + P
            print "Clause ", clause
            # print "Symbol ", symbols
            return dpllImplementation(clause, symbols, model)
        print "Clause ", clause
        P = findUnitClause(clause, model)

        if P:

            model.add(str(P))
            if symbols:
                removeSymbol(symbols, P)
            print "Unit Symbol : " + P
            print "Clause ", clause
            # print "Symbol ", symbols
            return dpllImplementation(clause, symbols, model)

        if not symbols:
            print "One of the output is ", model
            return True
        if not clause:
            print "One of the output is ", model
            return True
        first = symbols.pop()
        removeSymbol(symbols, first)
        # print "CALLING DPLL FOR AMBIGUOUS CASE"
        print "Popping : ", first
        # print "symbols : ", symbols
        # print "Clause : ", clause
        return dpllImplementation(clause, symbols, model_union(model, first, 1)) or dpllImplementation(clause, symbols, model_union(model, first, 2))

print player
print guest, table

guestOneTable()

for line in file_read:
    relation = list(line.strip().split())
    p1,p2,rel = relation
    cnfModeling(p1, p2, rel)

print "Final output"
print cnfList
print len(cnfList)
print main_symbols

sat_status = dpllImplementation(cnfList, main_symbols, main_model)
print "DPLL return status : ", str(sat_status)
