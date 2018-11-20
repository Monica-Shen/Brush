# 从数据库获取的部件数据
# test=[]
# test.append({'type': 'button', 'content': '', 'pointX': 0.5466269841269841, 'pointY': 0.7579365079365079, 'width': 0.09176587301587301, 'height': 0.14947089947089948})
# test.append({'type': 'label', 'content': '', 'pointX': 0.2490079365079365, 'pointY': 0.4973544973544973, 'width': 0.13541666666666666, 'height': 0.16534391534391535})
# 获取的用户屏幕分辨率
# screenResolutionX=1500
# screenResolutionY=900

# 代码生成函数
# 输入参数为部件数据（数据库获取，类型为list），屏幕分辨率长和宽
# 返回值为代码string

def codeBuilding(data, screenResolutionX, screenResolutionY):
    # 记录三种部件的数量，以区别部件的id
    countButton = 0
    countLabel = 0
    countInput = 0
    currentId = ""

    code = "<!DOCTYPE html> \n<html>\n"
    for component in data:
        code = code \
               + '<button type=' \
               + component['type'] \
               + ' style="width:' \
               + str(component['width'] * screenResolutionX) \
               + 'px;height:' \
               + str(component['height'] * screenResolutionY) \
               + 'px;background:#99ff00;\nposition:absolute;\nleft:' \
               + str(component['pointX'] * screenResolutionX) \
               + 'px;\ntop:' \
               + str(component['pointY'] * screenResolutionY) \
               + 'px;">' \
               + component['content'] \
               + '</' \
               + component['type'] \
               + '>\n'
    code += '</HTML>'
    return code

# codeBuilding(test,screenResolutionX,screenResolutionY)

