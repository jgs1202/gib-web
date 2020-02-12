# -*- coding: utf-8 -*-

import os
import math
import json
import networkx as nx
from PRISM import main as prism
from statistics import mean
from resize import sizing

# forcelayout (pythonライブラリ)を使えば良い結果が出るかも


def force(data, width, height, groups):
    G = nx.Graph()
    length = len(data['groups'])
    G.add_nodes_from([i for i in range(length)])
    linkNum = count_link(data)
    for i in range(len(linkNum)):
        for j in range(len(linkNum[i])):
            if linkNum[i][j] != 0:
                G.add_edge(i, i + j + 1, weight=linkNum[i][j])

    # 座標の決定
    pos = nx.spring_layout(G)  #, k=1/len(data['nodes']))
    xs, ys = [], []
    for i in range(length):
        temp = pos[i]
        xs.append(temp[0])
        ys.append(temp[1])
    for i in range(length):
        pos[i] *= 200
        pos[i][0] += 450
        pos[i][1] += 300

    area = width * height * 0.2
    unit = area / len(data['nodes'])
    for i in range(length):
        data['groups'][i]['dx'] = math.sqrt(unit * len(groups[i]))
        data['groups'][i]['dy'] = data['groups'][i]['dx']
        data['groups'][i]['x'] = pos[i][0]
        data['groups'][i]['y'] = pos[i][1]

    data = prism(data, linkNum, width, height)
    return data


def count_link(data):
    boxNum = len(data['groups'])
    linkNum = []
    for i in range(boxNum):
        linkNum.append([])
        for j in range(boxNum - i):
            linkNum[i].append(0)
    links = data['links']
    # print(len(links))
    for i in links:
        source = data['nodes'][i['source']]['group']
        target = data['nodes'][i['target']]['group']
        if source != target:
            if source < target:
                if linkNum[source][target - source] == 0:
                    linkNum[source][target - source] = 1
                else:
                    linkNum[source][target - source] += 1
            else:
                if linkNum[target][source - target] == 0:
                    linkNum[target][source - target] = 1
                else:
                    linkNum[target][source - target] += 1
    return linkNum

if __name__ == '__main__':
    width = 960
    height = 600
    for i in os.listdir('../data/'):
        if i[-5:] == '.json':
            data = json.load(open('../data/' + i))
            break

    groups = [[] for i in range(len(data['groups']))]
    for i in range(len(data['nodes'])):
        dic = {}
        dic['number'] = i
        dic['id'] = i
        groups[data['nodes'][i]['group']].append(dic)
    data = force(data, 960, 600, groups)
    import pylab as pl
    pl.xticks([0, width])
    pl.yticks([0, height])
    for i in data['groups']:
        pl.gca().add_patch(pl.Rectangle(xy=[i['x'], i['y']], width=i['dx'], height=i['dy'], linewidth='1.0', fill=False))
    pl.show()

    data = sizing(data)

    import pylab as pl
    pl.xticks([0, width])
    pl.yticks([0, height])
    for i in data['groups']:
        pl.gca().add_patch(pl.Rectangle(xy=[i['x'], height - i['y']], width=i['dx'], height=i['dy'], linewidth='1.0', fill=False))
    pl.show()
