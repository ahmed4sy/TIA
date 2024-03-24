import os
tmp = None
def rale(i=0, x:list=[]):
    return range(i,len(x))
def dict_loads(file:str):
    arr = file.read().split(', ')
    for i in range(len(arr)):
        if arr[i][0] == '{':
            arr[i] = arr[i].split('{')[1]
        if arr[i][len(arr[i])-1] == '}':
            arr[i] = arr[i].split('}')[0]
        arr[i] = arr[i].split(': ')

    rus = {}
    for i in rale(0,arr):
        rus[arr[i][0]] = arr[i][1]
    return rus
def dict_save(file = "open('go/to/path','w')", dict={}):
    tmp = str(dict).split("'")
    file.write(f'{tmp[0][0]}\n')
    for i in range(1,len(tmp)-1):
        if tmp[i][len(tmp[i])-1] == ',':
            file.write(f'\n{tmp[i]}')
        else:
            file.write(f'{tmp[i]}')
    file.write(f'\n{tmp[len(tmp)-1][len(tmp[len(tmp)-1])-1]}')
def sort_js(index:object):
    space = '   '
    reading = False
    tmp = 1
    text = f"{index[0]}\n{space}"
    for i in range(1,len(index)-1):
        if index[i] == "," and not reading:
            text += f"{index[i]}\n{space}"
        elif index[i] == "{" and not reading:
            tmp += 1
            text += f"{index[i]}\n{space*tmp}"
        elif index[i] == "}" and not reading:
            text += f"\n{index[i]}"
        elif index[i] == "[":
            text += f"{index[i]}"
            reading = True
        elif index[i] == "]":
            text += f"{index[i]}"
            reading = False
        else:
            text += f"{index[i]}"
    text += f"\n{index[len(index)-1]}"
    return text
def warp_text(sons:list = []):
    label:str = sons[0]
    for k in rale(1,sons):
        if len(sons[k]) >= 8:
            label += f"\n{sons[k]}\n"
        elif len(label.split(' '))%2 == 0:
           label += f"\n{sons[k]}"
        else:
            label += f" {sons[k]}"
    return label