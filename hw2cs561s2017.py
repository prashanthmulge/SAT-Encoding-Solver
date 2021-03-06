import math
import copy
from copy import deepcopy

file_read = open('input7.txt', 'r')
file_write = open('output.txt', 'w')

player = file_read.readline().strip().split()
guest = int(player[0])
table = int(player[1])
main_model = set([])
main_symbols = set([])
cnfList = []
output_log = ""


def cnfModeling(per1, per2, rel):
    print per1, per2, rel
    j = 1
    if rel == "F":
        while j <= table:
            subList = []
            subList.append("~X" + "-" + str(per1) + "-" + str(j))
            subList.append("X" + "-" + str(per2) + "-" + str(j))
            # symbols.add("~X" + str(relation[0]) + str(j))
            main_symbols.add("X" + "-" + str(per2) + "-" + str(j))
            cnfList.append(subList)
            # string = "~X" + str(relation[0]) + str(j) + "V" + "X" + str(relation[2]) + str(j)
            # cnfList.append(string)

            subList = []
            subList.append("X" + "-" + str(per1) + "-" + str(j))
            subList.append("~X" + "-" + str(per2) + "-" + str(j))
            main_symbols.add("X" + "-" + str(per1) + "-" + str(j))
            # symbols.add("~X" + str(relation[2]) + str(j))
            cnfList.append(subList)
            # string = "X" + str(relation[0]) + str(j) + "V" + "~X" + str(relation[2]) + str(j)
            # cnfList.append(string)
            j += 1
    else:
        while j <= table:
            subList = []
            subList.append("~X" + "-" + str(per1) + "-" + str(j))
            subList.append("~X" + "-" + str(per2) + "-" + str(j))
            main_symbols.add("X" + "-" + str(per1) + "-" + str(j))
            main_symbols.add("X" + "-" + str(per2) + "-" + str(j))
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
            subList1.append("X" + "-" + str(i) + "-" + str(j))
            main_symbols.add("X" + "-" + str(i) + "-" + str(j))
            # string1 += "X" + str(i) + str(j)
            subList2.append("~X" + "-" + str(i) + "-" + str(j))
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


def findPureSymbol(clauses, model):
    # print "Pure"
    toRemoveClause = []
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
                return del_clause
    return None


def findUnitClause(clauses, model):
    # print "Unit"
    toRemoveClause = []
    for clause_ele in clauses:
        if len(clause_ele) == 1:
            return clause_ele[0]
    return None


def formatOutput(oModel):
    global guest
    global output_log
    for i in range(0, guest):
        for j in oModel:
            ele = str(j).split("-")
            if ele[0] == "X" and ele[1] == str(i+1):
                output_log += "\n" + ele[1] + " " + ele[2]


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
        formatOutput(newModel)
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

    return copy.deepcopy(new_model)


def removeSymbol(new_symbol, str1):
    newTemp = set([])
    if str1[0] == "~":
        new_symbol.discard(str1[1:])
    else:
        new_symbol.discard(str1)
        for i in new_symbol:
            del_str = str(str1).split("-")
            ele = str(i).split("-")
            if del_str[1] == ele[1]:
                newTemp.add(i)
        for i in newTemp:
            new_symbol.discard(i)


def dpllImplementation(clause, symbols, model):
    # print "In DPLL"
    # print "In DPLL Clause : " , clause
    if not clause:
        formatOutput(model)
        print "One of the output is ", model
        return True
    ret = checkForTrueClause(clause, model)

    if ret == True:
        formatOutput(model)
        print "One of the output is ", model
        return True
    elif ret == False:
        return False
    else:
        # print "Clause ", clause
        P = findPureSymbol(clause, model)
        if P:
            model.add(str(P))
            if symbols:
                removeSymbol(symbols, P)
            # print "Pure Symbol : " + P
            # print "Clause ", clause
            # print "Symbol ", symbols
            return dpllImplementation(clause, symbols, model)
        # print "Clause ", clause
        P = findUnitClause(clause, model)

        if P:
            model.add(str(P))
            if symbols:
                removeSymbol(symbols, P)
            # print "Unit Symbol : " + P
            # print "Clause ", clause
            # print "Symbol ", symbols
            return dpllImplementation(clause, symbols, model)

        if not symbols:
            formatOutput(model)
            print "One of the output is ", model
            return True
        if not clause:
            formatOutput(model)
            print "One of the output is ", model
            return True
        first = symbols.pop()
        removeSymbol(symbols, first)
        # print "CALLING DPLL FOR AMBIGUOUS CASE"
        # print "Popping : ", first
        # print "symbols : ", symbols
        # print "Clause : ", clause
        return dpllImplementation(clause, copy.deepcopy(symbols), model_union(model, first, 1)) \
               or dpllImplementation(clause, copy.deepcopy(symbols), model_union(model, first, 2))

# print player
# print guest, table

guestOneTable()

for line in file_read:
    relation = list(line.strip().split())
    p1,p2,rel = relation
    cnfModeling(p1, p2, rel)

# print "Final output"
# print cnfList
# print len(cnfList)
# print main_symbols

sat_status = dpllImplementation(cnfList, main_symbols, main_model)
print "DPLL return status : ", str(sat_status)
if sat_status:
    file_write.write("yes" + "\n")
else:
    file_write.write("no" + "\n")

print output_log[1:]
file_write.write(output_log[1:])