import os, django
from django.db.models import Count

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

#网页信息管理模块


from server.models import *


#接口1：注册网页 输入：账户id
#返回内容包括：注册操作信息状态码，注册操作信息内容，网页id
def pageRegister(userID):
    select_result = WebPage.objects.filter(webPage_account_id=userID).count()
    userID_rt = ''
    content_rt = ''
    if (select_result>100):
        #已达可创建网页最大数
        status = False
        content_rt = 'Webs are enough!'
    else:
        #注册网页成功
        the_model = WebPage(webPage_account_id=userID)
        the_model.save()
        status = True
        content_rt = "register success!"
        userID_rt = userID

    result_dict = {
        'status': status,
        'content': content_rt,
        'userID': userID_rt,
    }
    return result_dict

#接口2：向网页增加控件  输入：网页id，控件内容，账户id
#返回内容包括：增加操作信息状态码，增加操作信息内容，网页id
def insertWedget(pageID, pageContent, userID):
    select_result = WebPage.objects.filter(webPage_pageid=pageID)
    userID_rt = ''
    content_rt = ''
    if not select_result:
        #网页不存在
        content_rt = "Page doesn't exist!"
        status = False
    elif(select_result[0].webPage_account_id != userID):
        #网页所对应传过来的账户id不一致
        content_rt = "Page and account doesn't match!"
        status = False
    else:
        #添加成功
        the_model = select_result[0]
        the_model.webPage_widget = pageContent
        the_model.save()
        content_rt = "insert successfully!"
        status = True
        userID_rt = userID

    result_dict = {
        'status': status,
        'content': content_rt,
        'userID': userID_rt,
    }
    return result_dict

#接口3：查询网页控件  输入：网页id，账户id
#返回内容包括：查询操作信息状态码，查询操作信息内容，网页id
def queryWedget(pageID, userID):
    select_result = WebPage.objects.filter(webPage_pageid=pageID)
    status = False
    content_rt = ''
    userID_rt = ''
    if not select_result:
        # 网页不存在
        content_rt = "Page doesn't exist!"
    elif (select_result[0].webPage_account_id != userID):
        # 网页所对应传过来的账户id不一致
        content_rt = "Page and account doesn't match!"
    else:
        # 查询成功
        status = True
        userID_rt = userID
        content_rt = select_result[0].webPage_widget  #查询成功返回控件内容
        print(content_rt)

    result_dict = {
        'status': status,
        'content': content_rt,
        'userID': userID_rt,
    }
    return result_dict

#接口4：查询账户已拥有网页列表 输入：账户id
#返回内容包括：查询操作信息状态码，查询操作信息内容，账户id
def queryPage(userID):
    select_result = WebPage.objects.filter(webPage_account_id=userID)
    status = False
    content_rt = ''
    userID_rt = ''
    if not select_result:
        # 网页不存在
        content_rt = "You have no page!"
    else:
        # 查询成功
        status = True
        userID_rt = userID
        content_rt = select_result  # 查询成功返回控件内容

    result_dict = {
        'status': status,
        'content': content_rt,
        'userID': userID_rt,
    }
    return result_dict


def demo(userID):
    select_result = WebPage.objects.filter(webPage_account_id=userID)
    if not select_result:
        the_model = WebPage(webPage_account_id=userID, webPage_pageid='001')
        the_model.save()
