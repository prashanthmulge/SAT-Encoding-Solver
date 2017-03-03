import math
import copy

file_read = open('input5.txt', 'r')
file_write = open('output.txt', 'w')

player = file_read.readline().strip().split()
guest = int(player[0])
table = int(player[1])
cnfList = []


def cnfModeling(relation):
    print relation, relation[4], relation[0], type(relation[2])
    j = 1
    if relation[4] == "F":
        while j <= table:
            string = "~X" + str(relation[0]) + str(j) + "V" + "X" + str(relation[2]) + str(j)
            cnfList.append(string)

            string = "X" + str(relation[0]) + str(j) + "V" + "~X" + str(relation[2]) + str(j)
            cnfList.append(string)
            j += 1
    else:
        while j <= table:
            string = "~X" + str(relation[0]) + str(j) + "V" + "~X" + str(relation[2]) + str(j)
            cnfList.append(string)
            j += 1


def guestOneTable():
    i = 1
    while i <= guest:
        j = 1
        string1 = ""
        string2 = ""
        while j <= table:
            string1 += "X" + str(i) + str(j)

            string2 += "~X" + str(i) + str(j)
            if j < table:
                string1 += "V"
                string2 += "V"

            j += 1
        cnfList.append(string1)
        cnfList.append(string2)
        i += 1


print player
print guest, table

guestOneTable()
print cnfList

for line in file_read:
    relation = list(line.strip())
    cnfModeling(relation)

print "Final output"
print cnfList
print len(cnfList)


