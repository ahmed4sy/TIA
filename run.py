#!/bin/python3.10
from ALG.index import bubbles,group
from PIL import Image,ImageDraw,ImageFont
from os import system as sys
from easyocr import Reader
from cv2 import imread
import json
from ALG.libAF import *
sys("clear")
#front end
v2 = None
print('With TIA you can now return all the (comic-book,manga,manhoa... and more) translating for arabic\nuse this command: LANG::PATH::[NAME-DIR] OR replace')
while True:
    v2 = input('TIA, COMMAND:')
    if v2 =='help':
        print('LANG (example): en(english),ar(arabic)\nPATH (example): ~/download/images')
    elif v2 == "replace":
        None
    elif v2 == "cle":
        sys('rm -r output/*')
    elif v2 == 'exit':
        quit()
    elif len(v2.split('::')) == 3:
        sys('rm -r DataImage')
        sys('mkdir DataImage')
        break
    else:
        print('TIA-ERORR: CommandError')
#var
index = v2.split('::')
sys(f'ls {index[1]} > Nameimgs')
sys('echo {} > dialogs.json')
rjs = open('dialogs.json','r').read()
wjs = open('dialogs.json','w')
LT = open('Nameimgs','r').readlines()
jso = json.loads(rjs)
sys(f"mkdir output/{index[2]}")
for i in rale(0,LT):
    jso[f"img{i+1}"] = {}
    p =LT[i].split("\n")[0]
    file_path = f"{index[1]}/{p}"
    lang = index[0]
    label = None
    pointer = None
    #objects
    try:
        rdr = Reader([lang.lower()],gpu=False)
    except:
        try:
            rdr = Reader([lang.lower()[0]+lang.lower()[1]],gpu=False)
        except:
            print(f'TIA-ERORR: this "{lang}" is not language')
            quit()
    sys("clear")
    print(f'{i}/{len(LT)} ', end='')
    print("loading...")
    img = imread(file_path)
    list = rdr.readtext(img)
    bub = bubbles(list)
    # .... .... ...... ...............
    img = Image.open(file_path)
    draw = ImageDraw.Draw(img)
    #drawing text

    for j in rale(0,bub):
        father = group(img,bub[j])[0]
        if father == 1:
            print(f'TIA-ERORR: Internet failed:: bub({j+1})')
            v3 = input('do you want to continue? (y/n):')
            if v3 == 'y':
                continue
            else:
                quit()
        elif father == '':
            continue
        else:
            fontsize = group(img,bub[j])[3]
            font = ImageFont.truetype('/usr/share/fonts/truetype/kacst/KacstLetter.ttf',fontsize)
            pointer = bub[j]
            color = group(img,bub[j])[2]
            fic = group(img,bub[j])[1]
            xyr = (pointer[0]+20,pointer[1],pointer[2]-20,pointer[3])
            xyl = (pointer[0]+35,pointer[1],pointer[2],pointer[3])
            sons = father.split(' ')
            label = warp_text(sons)
            draw.rectangle(xyr,fill=fic)
            draw.text(xyl,label,fill=color,font=font,align='center',spacing=4)
            # jso[f"img{i+1}"][f"d{j}"] = [label,pointer]
    # saving files
    img.save(f'output/{index[2]}/{i+1}.png')
sys("clear")
# strjs = json.dumps(jso)
# wjs.write(sort_js(strjs))
try:
    print(f'{i+1}/{len(LT)} ', end='')
except:
    print(f"TIA-ERORR: not found this dir:{index[1]}")
    quit()
print('done!')
input()
sys('rm Nameimgs')
sys('rm img.png')