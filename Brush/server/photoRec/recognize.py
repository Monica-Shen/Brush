import pytesseract
import PIL
from PIL import Image
import cv2
import numpy as np
import sys
import random
img = cv2.pyrDown(cv2.imread("C:/Users/lyhmj/Desktop/y.png", cv2.IMREAD_UNCHANGED))
# threshold 函数对图像进行二化值处理，由于处理后图像对原图像有所变化，因此img.copy()生成新的图像，cv2.THRESH_BINARY是二化值
ret, thresh = cv2.threshold(cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
# findContours函数查找图像里的图形轮廓
# 函数参数thresh是图像对象
# 层次类型，参数cv2.RETR_EXTERNAL是获取最外层轮廓，cv2.RETR_TREE是获取轮廓的整体结构
# 轮廓逼近方法
# 输出的返回值，image是原图像、contours是图像的轮廓、hier是层次类型
kernel_dilated=cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
kernel_eroded=cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
#使用dilated为腐蚀运算可以去除杂点 eroded为膨胀运算可以用来连接被分开的元素
dilated=cv2.dilate(thresh,kernel_dilated)
thresh=cv2.erode(dilated,kernel_eroded)
cv2.namedWindow("thresh",0)
cv2.imshow("thresh", thresh)
image, contours, hier = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
intx=[]
inty=[]
inta=[]
intb=[]
intw=[]
inth=[]
Stringcode=[]
Htmlkind=[]
Rectanglex=[]
Rectangley=[]
Rectanglew=[]
Rectangleh=[]
m=0
# 不重复的矩形框的数量
q=0
union_x=0
union_y=0
union_w=0
union_h=0
codeNumber=0
for c in contours:
    a, b, c, d = cv2.boundingRect(c)
    p_x=a+c
    p_y=b+d
for c in contours:
    # 轮廓绘制方法一
    # boundingRect函数计算边框值，x，y是坐标值，w，h是矩形的宽和高
    x, y, w, h = cv2.boundingRect(c)
    picture_x = x + w
    picture_y = y + h
    if x+w>p_x-10:
        mjx=1
    else:
     m = m + 1
     intx.append(x)
     inty.append(y)
     intw.append(w)
     inth.append(h)
    # 在img图像画出矩形，(x, y), (x + w, y + h)是矩形坐标，(0, 255, 0)设置通道颜色，2是设置线条粗度
    # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
print("矩形的个数为",m)
print("图像横坐标为", p_x, "图像纵坐标为", p_y)
def union(a,b):
    union_x=min(intx[a],intx[b])
    union_y=min(inty[a],inty[b])
    union_w=max(intx[a]+intw[a],intx[b]+intw[b])-union_x
    union_h=max(inty[a]+inth[a],inty[a]+inth[b])-union_y
    intx[a]=union_x
    inty[a]=union_y
    intw[a]=union_w
    inth[a]=union_h
    intx[b]=union_x
    inty[b]=union_y
    intw[b]=union_w
    inth[b]=union_h
#监测两个矩形框是否覆盖
def Iscover(a,b):
    #横坐标轴上不覆盖
    if intx[a]+intw[a]<intx[b] or intx[b]+intw[b]<intx[a]:
        mjx=1
    #纵坐标轴上不覆盖
    elif inty[a]+inth[a]<inty[b] or inty[b]+inth[b]<inty[a]:
        mjx=1
    #这两个矩形框有覆盖要合并
    else:
        union(a,b)
#开始进行合并
for union_i in range(0,5000):
    j=random.randint(0,m-1)
    g=random.randint(0,m-1)
    # print(j)
    # print(g)
    Iscover(j,g)
for rectangle_i in range(0,m-1):
    #判断并去除重复的边框
    bool_rectangle=1
    if rectangle_i>0:
          for number_rectangle in range(0,rectangle_i):
              if intx[rectangle_i]==intx[number_rectangle]:
                  # bool_rectangle=0说明此矩形与之前重复了
                  bool_rectangle=0

    # print(intx[rectangle_i])
    # 当矩形框不重复时执行以下语句
    if bool_rectangle==1:
        # 排除过于小的边框
      if intw[rectangle_i]<p_x/15:
        intw[rectangle_i]=0
        inth[rectangle_i]=0
      elif inth[rectangle_i]<p_y/15:
        intw[rectangle_i] = 0
        inth[rectangle_i] = 0
      else:
       q=q+1
       print("这是第",q,"个矩形")
       print("横坐标为", intx[rectangle_i], "纵坐标为", inty[rectangle_i])
       print("矩形的宽为", intw[rectangle_i], "矩形的高为", inth[rectangle_i])
       cv2.rectangle(img, (intx[rectangle_i], inty[rectangle_i]),
                      (intx[rectangle_i] + intw[rectangle_i], inty[rectangle_i] + inth[rectangle_i]), (0, 255, 0), 5)
       Rectanglex.append(intx[rectangle_i])
       Rectangley.append(inty[rectangle_i])
       Rectangleh.append(inth[rectangle_i])
       Rectanglew.append(intw[rectangle_i])

       #img_nlt为截取的边框之内的图片
       img_nlt = img[inty[rectangle_i]:inty[rectangle_i] + inth[rectangle_i],
               intx[rectangle_i]:intx[rectangle_i] + intw[rectangle_i]]
       #对截取的图片进行二化处理
       ret, img_nlt_thresh = cv2.threshold(cv2.cvtColor(img_nlt.copy(), cv2.COLOR_BGR2GRAY), 160, 255, cv2.THRESH_BINARY)
       cv2.imshow("picture cutted with thresh", img_nlt_thresh)
       #获取边框内部的文本内容,lang后跟自己选择的数据量库
       code = pytesseract.image_to_string(img_nlt_thresh, lang="eng")
       #如果code不为空那么向数组中添加这条记录
       if code=="":
        Stringcode.append(code)
       # 框中文本的数量
        codeNumber=codeNumber+1
for cc in range(0,codeNumber):
    if Stringcode[cc] in "button":
        Htmlkind.append(1)
        #strip函数用于去除字符串开头的button文本
        Stringcode[cc]=Stringcode[cc].strip("button")
    if Stringcode[cc] in "input":
        Htmlkind.append(2)
        #strip函数用于去除字符串开头的input文本
        Stringcode[cc] = Stringcode[cc].strip("input")
    if Stringcode[cc] in "text":
        Htmlkind.append(3)
        #stript函数用于去除字符串开头的text文本
        Stringcode[cc] = Stringcode[cc].strip("text")

#框的总个数为codenumber，框的长宽高分别为 Rectanglex[],Rectangley[],Rectangleh[],Rectanglexw[],框的类型为Htmlkind[],框的文本内容为Stringcode[cc]

# ret, thresh = cv2.threshold(cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
# image, contourss, hier = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
# print(len(contourss))
print("矩形的总个数为", q)
# 显示图像
cv2.namedWindow("contours",0)
cv2.imshow("contours", img)
cv2.waitKey()
cv2.destroyAllWindows()
