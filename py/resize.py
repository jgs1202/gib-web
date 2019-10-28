# -*- coding: utf-8 -*-

import os
import json
import numpy as np
import sys


def sizing(data):
    print(data['groups'])
    width = 1620.7
    width = 960
    height = 600
    height = 1000
    outWidth = 920
    outHeight = 560
    margin = 20
    sizes = []
    old = (len(data['groups']))

    first = 0
    for i in data['groups']:
        if first == 0:
            first += 1
            xmin = i['x']
            xmax = xmin + i['dx']
            ymin = i['y']
            ymax = ymin + i['dy']
        else:
            if i['x'] < xmin and i['x']:
                xmin = i['x']
            if i['x'] + i['dx'] > xmax:
                xmax = i['x'] + i['dx']
            if i['y'] < ymin:
                ymin = i['y']
            if i['y'] + i['dy'] > ymax:
                ymax = i['y'] + i['dy']

    reWidth = xmax - xmin
    reHeight = ymax - ymin
    reAspect = reWidth / reHeight
    trueAspact = outWidth / outHeight
    if reAspect > trueAspact:
        which = 'x'
    else :
        which = 'y'
    # print(xmin, xmax, ymin, ymax, reWidth, reHeight)
    if which == 'x':
        # print('width')
        span = (reWidth * outHeight / outWidth - reHeight)/2
        ymin -= span
        ymax += span
        reHeight = reWidth * height / width
        ratio = (outHeight) / reHeight
    if which == 'y':
        # print('height')
        span = (reHeight * outWidth / outHeight - reWidth)/2
        xmin -= span
        xmax += span
        reWidth = reHeight * width / height
        ratio = outHeight / reHeight

    # print(xmin, xmax, ymin, ymax, reWidth, reHeight)

    if which == 'x':
        for i in  range(len(data['groups'])):
            data['groups'][i]['x'] = (data['groups'][i]['x'] - xmin) * ratio
            data['groups'][i]['y'] = (data['groups'][i]['y'] - ymin - span) * ratio
            data['groups'][i]['dx'] *= ratio
            data['groups'][i]['dy'] *= ratio
            # data['groups'][i]['x'] = (data['groups'][i]['x'] - xmin - span)
            # data['groups'][i]['y'] = (data['groups'][i]['y'] - ymin)
    if which == 'y':
        for i in  range(len(data['groups'])):
            data['groups'][i]['x'] = (data['groups'][i]['x'] - xmin - span) * ratio
            data['groups'][i]['y'] = (data['groups'][i]['y'] - ymin) * ratio
            data['groups'][i]['dx'] *= ratio
            data['groups'][i]['dy'] *= ratio
    # print(ratio)


    for i in range(len(data['groups'])):
        if which == 'x':
            data['groups'][i]['x'] += margin
            data['groups'][i]['y'] += margin + span * ratio
        if which == 'y':
            data['groups'][i]['x'] += margin + span*ratio
            data['groups'][i]['y'] += margin

    # print(span, (outWidth - reWidth)/2)
    # print(reWidth, reHeight)

    first = 0
    for i in data['groups']:
        if first == 0:
            first += 1
            xmin = i['x']
            xmax = xmin + i['dx']
            ymin = i['y']
            ymax = ymin + i['dy']
        else:
            if i['x'] < xmin and i['x']:
                xmin = i['x']
            if i['x'] + i['dx'] > xmax:
                xmax = i['x'] + i['dx']
            if i['y'] < ymin:
                ymin = i['y']
            if i['y'] + i['dy'] > ymax:
                ymax = i['y'] + i['dy']
    # print(data['groups'])
    dic = {}
    dic['x'] = 0
    dic['y'] = 0
    dic['dx'] = outWidth + margin*2
    dic['dy'] = outHeight + margin*2
    data['groups'].append(dic)
    # for i in range(len(data['nodes'])):
    #     data['nodes'][i]['cx'] += margin
    #     data['nodes'][i]['cy'] += margin

    sizes.append(data['groupSize'])

    return data


def main():
    main = '../data/FDGIB/temp/'
    global sizes
    sizes = []
    # for dir in os.listdir(main):
    #     if (dir != '.DS_Store'):
    num = 0
    for file in os.listdir(main):
        if file[-5:] == '.json':
            print(file)
            path = main + file
            # print(path)
            resize(path, num, main)
            num += 1
    print(sizes.count(8), sizes.count(17))

if __name__ == '__main__':
    global width
    global height
    global outWidth
    global outHeight
    width = 1620.7
    height = 1000
    outWidth = 920
    outHeight = 560
    main()
