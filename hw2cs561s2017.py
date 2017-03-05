import math
import copy
from copy import deepcopy
from sets import Set

file_read = open('input.txt', 'r')
file_write = open('output.txt', 'w')

player = file_read.readline().strip().split()
guest = int(player[0])
table = int(player[1])
model = Set([])
symbols = Set([])
cnfList = []


def cnfModeling(relation):
    print relation, relation[4], relation[0], type(relation[2])
    j = 1
    if relation[4] == "F":
        while j <= table:
            subList = []
            subList.append("~X" + str(relation[0]) + str(j))
            subList.append("X" + str(relation[2]) + str(j))
            symbols.add("~X" + str(relation[0]) + str(j))
            symbols.add("X" + str(relation[2]) + str(j))
            cnfList.append(subList)
            # string = "~X" + str(relation[0]) + str(j) + "V" + "X" + str(relation[2]) + str(j)
            # cnfList.append(string)

            subList = []
            subList.append("X" + str(relation[0]) + str(j))
            subList.append("~X" + str(relation[2]) + str(j))
            symbols.add("X" + str(relation[0]) + str(j))
            symbols.add("~X" + str(relation[2]) + str(j))
            cnfList.append(subList)
            # string = "X" + str(relation[0]) + str(j) + "V" + "~X" + str(relation[2]) + str(j)
            # cnfList.append(string)
            j += 1
    else:
        while j <= table:
            subList = []
            subList.append("~X" + str(relation[0]) + str(j))
            subList.append("~X" + str(relation[2]) + str(j))
            symbols.add("~X" + str(relation[0]) + str(j))
            symbols.add("X" + str(relation[2]) + str(j))
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
            symbols.add("X" + str(i) + str(j))
            # string1 += "X" + str(i) + str(j)
            subList2.append("~X" + str(i) + str(j))
            if table > 1:
                symbols.add("~X" + str(i) + str(j))
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
    if not symbols:
        return None
    isPure = 0
    for clause_ele in clauses:
        isPure = 1
        for del_clause in clause_ele:
            if del_clause[0] == "~":
                if del_clause[1:] in symbols:
                    isPure = 0
                    break
            else:
                if ("~" + del_clause ) in symbols:
                    isPure = 0
                    break
            if isPure:
                model.add(del_clause)
                for j in clauses:
                    if del_clause in j:
                        clauses.remove(j)
                return del_clause
    return None




def findUnitClause(clauses, model):
    print "Unit", clauses
    for clause_ele in clauses:
        if len(clause_ele) == 1:
            model.add(clause_ele[0])
            for del_clause in clauses:
                if clause_ele[0] in del_clause:
                    clauses.remove(del_clause)
                else:
                    if clause_ele[0][0] == "~":
                        if clause_ele[0][1:] in del_clause:
                            del_clause.remove(clause_ele[0][1:])
                    else:
                        if ("~" + clause_ele[0]) in del_clause:
                            del_clause.remove("~" + clause_ele[0])
            return clause_ele[0]
    return None


def checkForTrueClause(clause, model):
    if not model:
        return "Cont"
    toRemove = []
    for mod_ele in model:
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
        print "One of the output is ", model
        return True

    for c in clause:
        if not c:
            return False

    for ele in toRemove:
        clause.remove(ele)
    return "Cont"


def model_union(model, pop_str, type):
    if type == 1:
        model.add(pop_str)
    else:
        if pop_str[0] == "~":
            model.add(pop_str[1:])
        else:
            model.add("~" + pop_str)

    return deepcopy(model)


def dpllImplementation(clause, symbols, model):
    print "In DPLL"
    if not symbols:
        return False
    print "In DPLL Clause : " , clause
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
        P = findPureSymbol(clause, symbols, model)
        if P:

            model.add(str(P))
            if symbols:
                symbols.discard(P)
            print "Pure Symbol : " + P
            print "Clause ", clause
            print "Symbol ", symbols
            return dpllImplementation(clause, symbols, model)

        P = findUnitClause(clause, model)

        if P:
            print "Unit Symbol : " + P
            print "Clause ", clause
            print "Symbol ", symbols
            model.add(str(P))
            if symbols:
                symbols.discard(P)
            return dpllImplementation(clause, symbols, model)

        if not symbols:
            print "One of the output is ", model
            return True
        if not clause:
            print "One of the output is ", model
            return True
        first = symbols.pop()
        symbols.discard(first)
        print "CALLING DPLL FOR AMBIGIOUS CASE"
        print "Popping : ", first
        print "symbols : ", symbols
        print "Clause : ", clause
        return dpllImplementation(clause, symbols, model_union(model, first, 1)) or dpllImplementation(clause, symbols, model_union(model, first, 2))

print player
print guest, table

guestOneTable()
print cnfList
print symbols

for line in file_read:
    relation = list(line.strip())
    cnfModeling(relation)

print "Final output"
print cnfList
print len(cnfList)
print symbols

sat_status = dpllImplementation(cnfList, symbols, model)
print "DPLL return status : ", sat_status
