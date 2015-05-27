#!/usr/bin/env python
from subprocess import Popen, PIPE, STDOUT

commandsA = [
  'userA <- qloud [label="sync", linecolour="blue"];',
  'userA rbox userA [label="edit", textbgcolour="aqua" ];',
  'userA -> qloud [label="sync", linecolour="blue"];',
  'userA <- qloud [label="sync", linecolour="blue"];'
]

commandsB = [
  'userB <- qloud [label="sync", linecolour="blue"];',
  'userB rbox userB [label="delete", textbgcolour="red" ];',
  'userB -> qloud [label="sync", linecolour="blue"];',
  'userB <- qloud [label="sync", linecolour="blue"];'
]

header = 'msc { hscale = "2";\nuserA,qloud,userB;\nuserA box userB [label="has machine", textbgcolour="green"]; '
footer = ' userA note userB [label="?"]; }'

def popAndRecurse(listToPop, otherList):
    result = []
    short = list(listToPop)
    command = short.pop(0)
    branches = mergeLists(short, otherList)
    for branch in branches:
        branch.insert(0, command)
        result.append(branch)
    return result


def mergeLists(listA, listB):
    listA = list(listA)
    listB = list(listB)
    if len(listA) == 0 and len(listB) == 0:
        return [[]]

    result = []
    if len(listA) > 0:
        result += popAndRecurse(listA, listB)

    if len(listB) > 0:
        result += popAndRecurse(listB, listA)

    return result

def createFile(inputData, filename):
    p = Popen(['mscgen', '-T', 'png', '-o', filename], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    throwAway = p.communicate(input=header+inputData+footer)

result = mergeLists(commandsA, commandsB)
count = 0

for trace in result:
    createFile("\n".join(trace), 'trace-'+str(count)+'.png')
    count += 1
