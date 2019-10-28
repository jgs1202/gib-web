# -*- coding: utf-8 -*-

import sys
import os
import math
from .STGIB import ST
from .Chaturvedi import Chatu
from .TRGIB import TR
import json
import time
import random
from .add_coordinates import add
from .FDGIB import force
from .resize import sizing


def application(data):
    data = json.loads(data.decode('utf-8'))
    if 'dx' in data['data']['groups'][0]:
        if data['data']['groups'][-1]['dx'] > 900:
            del data['data']['groups'][-1]
    nodes = data['data']['nodes']
    length = len(data['data']['nodes'])
    maxGroup = 0
    width = 960
    height = 600

    # get length of group
    for i in range(length):
        current = nodes[i]['group']
        if current > maxGroup:
            maxGroup = current
    groups = [[] for i in range(maxGroup + 1)]

    # make list 'groups' a list have nodes' index
    for i in range(length):
        dic = {}
        dic['number'] = i
        groups[nodes[i]['group']].append(dic)

    with_box = classify(data, groups, width, height)
    os.chdir('rust-fd-layout')
    os.system('pwd')
    file = '../data/' + str(math.floor(time.time())) + str(math.floor(random.random())) + '.json'
    f = open(file, 'w')
    json.dump(with_box, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()
    cmd = 'cargo run --release --example gib-cli -- -f ' + file + ' > ' + file[:-5] + '-nodes.txt'
    os.system(cmd)
    data = add(file)
    cmd = ['rm ' + file, 'rm ' + file[:-5] + '-nodes.txt']
    for i in cmd:
        os.system(i)
    os.chdir('/home/jgs_kuee/gib-web')

    return data


def classify(data, groups, width, height):
    if data['layout'] == 'ST-GIB':
        out = ST(data['data'], groups, width, height)
    elif data['layout'] == 'CD-GIB':
        out = Chatu(data['data'], width, height)
    elif data['layout'] == 'TR-GIB':
        out = TR(data['data'], width, height, groups)
    if data['layout'] == 'FD-GIB':
        out = sizing(force(data['data'], width, height, groups))
    return out
