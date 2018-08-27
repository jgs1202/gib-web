# -*- coding: utf-8 -*-

import os
import json
import sys
from .DGIB import doughnut
from .CGIB import croissant
from .STGIB import ST
from operator import itemgetter

def Chatu(data, width, height):
    links = data['links']
    nodes = data['nodes']
    length = len(nodes)
    maxGroup = 0

    # get length of group
    for i in range(length):
        current = nodes[i]['group']
        if current > maxGroup:
            maxGroup = current
    groups = [ [] for i in range(maxGroup+1)]

    # make list 'groups' a list have nodes' index
    for i in range(length):
        dic = {}
        dic['number'] = i
        groups[nodes[i]['group']].append(dic)


    ###################### G-skewness ##########################
    Gskew = []
    for i in range(maxGroup + 1):
        Gskew.append([])
        for j in range(maxGroup + 1 - i):
            Gskew[i].append(0)
    for i in links:
        source = data['nodes'][i['source']]['group']
        target = data['nodes'][i['target']]['group']
        if source != target:
            if source < target:
                if Gskew[source][target-source] == 0:
                    # print('empty')
                    Gskew[source][target-source] = 1
                else:
                    Gskew[source][target-source] += 1
            else:
                if Gskew[target][source-target] == 0:
                    # print('empty')
                    Gskew[target][source-target] = 1
                else:
                    Gskew[target][source-target] += 1


    max = Gskew[0][0]
    length1 = len(Gskew)
    maxIndex = []
    for i in range(length1):
        length2 = len(Gskew[i])
        for j in range(length2):
            if Gskew[i][j] > max:
                max = Gskew[i][j]
                maxIndex = [i, j + i]

    G_skewness = max
    if len(maxIndex) != 0:
        G_skewness = (len(groups[maxIndex[0]]) + len(groups[maxIndex[1]])) / len(data['nodes'])
    else:
        G_skewness = 0

    ###################### G-degree ##########################

    length = len(groups)
    # print('Gskew is')
    # print(Gskew)
    Gdegree = [0.0 for i in range(length)]
    for i in range(length):
        len2 = len(Gskew)
        for j in range(len2):
            len3 = len(Gskew[j])
            for k in range(len3):
                if j == i:
                    if float(Gskew[j][k]) != 0.0:
                        Gdegree[i] += 1
                elif j < i:
                    if k == i-j:
                        if float(Gskew[j][k]) != 0.0:
                            Gdegree[i] += 1
    for i in range(len(Gdegree)):
        Gdegree[i] = [i, int(Gdegree[i])]
    Gdegree.sort(key=itemgetter(1), reverse=True)


    Gmax = 'null'
    nodesOfMax = []
    for aGroup in Gdegree:
        if Gmax != int(aGroup[1]):
            if len(nodesOfMax) != 0:
                nodesOfMax.sort(key=itemgetter(1), reverse=True)
                tempDegree = []
                for i in range(len(nodesOfMax)):
                    for j in range(len(groups)):
                        if nodesOfMax[i][0] == Gdegree[j][0]:
                            tempDegree.append(Gdegree[j])
                            break
                targetIndex = tempDegree[0][1]
                for i in range(len(Gdegree)):
                    if Gdegree[i][1] == targetIndex:
                        startingPoint = i
                        break
                for i in range(startingPoint, startingPoint + len(tempDegree)):
                    Gdegree[i] = tempDegree[i-startingPoint]
                nodesOfMax = []
            nodesOfMax.append([aGroup[0], len(groups[aGroup[0]])])
            Gmax = int(aGroup[1])
        else:
            nodesOfMax.append([aGroup[0], len(groups[aGroup[0]])])
    # print(Gdegree)
    # print(Gmax)

    #################### G-skewness ##############
    G_skewness = (len(groups[Gdegree[0][1]]) + len(groups[Gdegree[1][1]])) / len(data['nodes'])
    if len(groups) <= 3 or G_skewness < 0.1:
        type = 'STGIB'
        out = ST(data, groups, width, height)
    elif len(groups) > 3 and G_skewness >= 0.1 and G_skewness <= 0.45:
        type = 'DGIB'
        out = doughnut(data, groups, width, height, Gdegree)
    elif len(groups) > 3 and G_skewness > 0.45:
        type = 'CGIB'
        out = croissant(data, groups, width, height, Gdegree)
    print(type)
    return out


if __name__ == '__main__':
    main = '../data/origin/Chaturvedi/'
    global width
    global height
    width = 960
    height = 600
    num = 0
    # for dir in os.listdir(main):
        # if (dir != '.DS_Store'):
            # print(dir)
    for file in os.listdir(main):
        # print(file)
        dir = False
        if (dir != '.DS_Store'):
            # if num > 0:
            num += 1
            path = main + file
            width = 960
            height = 600
            readjson(path, dir, file)
