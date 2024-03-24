from googletrans import Translator
import os
import easyocr
from cv2 import imread,imwrite
from PIL import Image
rdr = easyocr.Reader(['en'],gpu=False)
trans = Translator()
dataocr = open('dataocr','r').read().split(';')
for p in range(len(dataocr)):
    dataocr[p] = dataocr[p].split(':')
x,y,w,h = 0,0,0,0
dicmal = [0,1,2,3,4,5,6,7,8,9]
num = 0
litters = ['a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','q','w','e','r','t','y','u','i','o','p']


def thisReal(dict,key)-> bool:
    try:
        dict[key]
        return True
    except:
        return False
def oneColor(img)->tuple:
    catalog = {
        f"{img[int((len(img)-1)/2)][0]}":1
    }
    for imNum in range(1,len(img[int((len(img)-1)/2)])):
        pixel = str(img[int((len(img)-1)/2)][imNum])
        if thisReal(catalog,pixel) == False:
            catalog[pixel] = 1
        else:
            catalog[pixel] += 1
    total = max(catalog.values())
    for catKey in catalog:
        if catalog[catKey] == total:
            tmp = catKey
            break
    colorList = tmp.split()
    colorList[0] = colorList[0].split('[')[1]
    colorList[2] = colorList[2].split(']')[0]
    res = (int(colorList[0]),int(colorList[1]),int(colorList[2]))
    return res

def group(file = 'path/to/file',points:list =(x,y,w,h)) -> tuple:
    global num
    lamp = False
    x,y,w,h = points[0]-25,points[1]-5,points[2],points[3]
    num += 1
    croped = (x,y,w,h)
    marks = ['+','%','@','#']
    img = file.crop(croped)
    img.save(f'img.png')
    img = imread(f'img.png')
    box = rdr.readtext(img)
    color = oneColor(img)
    area = (w-x) * (h-y)
    if color != (255,255,255):
        fill = (255,255,255)
    else:
        fill = (0,0,0)
    try:
        text = f'{box[0][1]}'.lower()
        percent = [box[0][2]]
    except IndexError:
        return '','','',''
    try:
        int(text)
        return '','','',''
    except:
        None
    for i in range(1,len(box)):
        if box[i][2] < 0.3:
            continue
        tmp = f'{box[i][1][0]}'
        for char in range(1,len(box[i][1])):
            if box[i][1][char] == 'i' and box[i][2] < 0.5:
                tmp += ''
            else:
                tmp += f'{box[i][1][char]}'
        if tmp in ['fi','ka','ja','++']:
            continue
        text += f" {tmp}".lower()
        percent.append(box[i][2])
        text = text.replace(':','');text = text.replace(';','');text = text.replace('_','');text = text.replace(']','');text = text.replace('[','');text = text.replace('.','');text = text.replace('+','')
        for ch in range(len(dataocr)-1):
            text = text.replace(dataocr[ch][0],dataocr[ch][1])


    if area > 70000 and len(text) < 35:
        fontsize = 84
    else:
        fontsize = 42

    try:
        label:str = trans.translate(str(text.lower()), dest='ar').text
        for char in label:
            for litter in litters:
                if char == litter:
                    label = label.replace(char,'')
            for dicm in dicmal:
                if char == str(dicm):
                    return '','','',''
        os.system('rm img.png')
        russ = (label,color,fill,fontsize)
        return russ
    except:
        return 1,1,1,1



def bubbles(ocr:list):
    descent = True
    root = [ocr[0][0]]
    tmp = ocr[0][0][0]
    list = []
    limitx = 100
    limity = 150
    n = 0
    Boolen = [True]
    on = False
    ls = 1
    for i in range(1,len(ocr)):
       Boolen.append(False)
    while descent:
        s = 0
        n += 1
        for i in range(ls,len(ocr)):
            if tmp[1] <= ocr[i][0][0][1] and  ocr[i][0][0][1] <= tmp[1]+limity and ocr[i][0][0][0]  <= tmp[0]+limitx and ocr[i][0][0][0]  >= tmp[0]-limitx:
                on = True
                Boolen[i] = True
                root.append(ocr[i][0])
                tmp = ocr[i][0][0]
        list.append(root)
        #error func
        if len(ocr) != len(Boolen):
            print("ERORR: BOOL")
            break
        if n == 100:
            print("ERORR: LOOP")
            print('bool:',Boolen)
            print('tmp:',tmp)
            break
        #try exit for loop
        for i in range(len(Boolen)):
            if Boolen[i] == False:
                tmp = ocr[i][0][0]
                Boolen[i] = True
                root = []
                ls = i
                break
            else:
                s+=1
                if s == len(Boolen):
                    descent = False
    # read array
    result = []
    tmp = list[0][0]
    limit = 100
    s = 0
    # end = len(list)
    # while s == end:
    #     for l in range(s,len(list)):
    #         if tmp[0][1] < list[l][0][0][1] and list[l][0][0][1] < tmp[0][1]+limit:
    #             tmp += list[l]
    #             list.remove(list[l])
    #     s+=1
    #     tmp = list[s][0]

    for r in range(len(list)):
        xtmp=list[r][0][0][0]
        ytmp=list[r][0][0][1]
        for lo in range(len(list[r])):
            if xtmp < list[r][lo][0][0]:
                xtmp+=list[r][lo][0][0]-xtmp
        X = xtmp
        Y = ytmp
        H = list[r][len(list[r])-1][2][1]
        W = list[r][len(list[r])-1][2][0]

        index =(X-55,Y-10,W+50,H+10)
        result.append(index)
    return result
print("this is lib, (RUN: run.py)")
# img =Image.open("/home/ahmed4s/Documents/Projects/TIA/c/Scott Pilgrim 01-010.jpg")
# lis = rdr.readtext(img)
# for j in range(len(bubbles(lis))):
#     for i in bubbles(lis)[j]:
#         print(i)
#     print('\n')
# for i in lis:
#     print(i)
# def test(ocr):
#     xyl = ocr[0][0]
#     tmp = (xyl[0][0], xyl[0][1],xyl[1][0]+100,xyl[2][1]+200)
#     img.crop(tmp).show()
# test(listreder)

# lista = [([[2,5],[5,3],[4,9]],'my',0.5),([[2,5],[5,3],[4,9]],'name',0.5),([[2,5],[5,3],[4,9]],'is',0.5),([[2,5],[5,3],[4,9]],'yousif',0.5)]

# from PIL import Image,ImageDraw,ImageFont
# import textwrap

# img = Image.open('ind.png')
# draw = ImageDraw.Draw(img)
# y = 10
# text = 'السلام عليكم'
# point = (10,y)
# color= (0,0,0)
# lines = textwrap.w(raptext,width=200,font=ImageFont.truetype('rubik.ttf',32))
# draw.rectangle(((0,0),(100,200)),fill='white')
# for line in lines:
#     draw.text(point,line,color,font=ImageFont.truetype('rubik.ttf',32))
#     y += ImageFont.truetype('rubik.ttf',32).gets
# img.show()



# cropImg = (0,100, 1000,1000)
# img = Image.open('1.jpg')
# img.crop(cropImg).show()


# from googletrans import Translator
# file = open('tran.txt','w')
# trans = Translator()
# text = trans.translate("tree for train", dest='ar').text
# file.write(text)
# print('done!')
# file.close


