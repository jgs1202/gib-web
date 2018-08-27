# -*- coding: utf-8 -*-
import json


def add(file):
    minus = False
    f = open(file[:-5] + '-nodes.txt')
    txt = f.read()
    reader = open(file)
    global data
    data = json.load(reader)
    length = len(data['nodes'])
    list = [i for i in range(length)]
    sentence = ''
    num = 0
    name = 0
    for i in txt:
        try:
            i = int(i)
        except:
            pass
        if type(i) == int:
            sentence += (str(int(i)))
        else:
            if i == '.':
                sentence = sentence + '.'
            elif i == '-':
                minus = True
                break
            else:
                if num == 0:
                    global dic
                    dic = {}
                    dic['cx'] = float(sentence)
                    sentence = ''
                    num += 1
                elif num == 1:
                    dic['cy'] = float(sentence)
                    sentence = ''
                    num = 0
                    list[name] = dic
                    name += 1
                else:
                    print('error')
    if minus:
        return 'error'

    else:
        for i in range(length):
            data['nodes'][i]['cx'] = list[data['nodes'][i]['name']]['cx']
            data['nodes'][i]['cy'] = list[data['nodes'][i]['name']]['cy']
        return data