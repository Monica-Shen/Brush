from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from database.account_management import interfaces as accm
from database.webpage_management import interfaces as webpm
from django.views.decorators.csrf import csrf_exempt
from server.photoRec import recognize as rec
from server.photoRec import codeBuilding as cobu
from server.photoRec import uploadImg as upimg

# def index(request):
#     return render(request, 'server/login.html')
# Create your views here.


def home(request):
    # request.Post
    # request.Get
    return render(request, 'home.html')

#账户登陆
@csrf_exempt #增加装饰器，作用是跳过 csrf 中间件的保护
def login(request):
    # request.Get
    if request.method== 'GET':
        return render(request, 'login.html')
    # request.Post
    if request.method=='POST':
        result = accm.login(request.POST.get('username'),request.POST.get('password'))
        if result['status']:
            response = HttpResponseRedirect('menu.html')
            response.set_cookie('user_id', request.POST.get('username'))
            return HttpResponse(result['content'])
        else:
            return HttpResponse(result['content'])


#账户注册  输入：用户名 密码 二次密码 email  输出：是否创建成功
def register(request):
    # request.Get
    if request.method=="GET":
        return render(request, 'register.html')
    # request.Post
    if request.method=="POST":
        user_id = request.POST.get('re_username')
        password = request.POST.get('re_password')
        pass_again = request.POST.get('re_passwordagain')
        email = request.POST.get('re_email')
        if(password != pass_again):
            return HttpResponse("password doesn't match!")
        else:
            result = accm.register(user_id, password, email)
            if result['status']:
                return HttpResponse(result['content'])
            else:
                return HttpResponse(False)


def menu(request):
    return render(request, 'menu.html')


#网页注册  输入：账户id  输出：是否创建成功
def pageRegister(request):
    # request.Get
    if request.method=="GET":
        return render(request, 'menu.html')  #网页注册界面/按钮
    # request.Post
    if request.method=="POST":
        user_id = request.POST.get('userID')
        result = webpm.pageRegister(user_id)
        if result['status']:
            return HttpResponse(result['content'])
        else:
            return HttpResponse(False)


#向网页增加控件  输入：网页ID，账户ID，图片  输出：是否添加成功
def addWedget(request):

    if request.method=="POST":
        user_id = request.POST.get('username')
        page_id = request.POST.get('pageID')
        img = request.POST.get('img')  # 前端打包过来的是路径 可修改
        upimg_rt = upimg.upload_image(page_id, img)
        if upimg_rt['success']:
            page_path = upimg_rt['path']
            page_content = rec.picProcess(page_path)
            result = webpm.insertWedget(page_id, page_content, user_id)
            return HttpResponse(result['content'])
        else:
            return HttpResponse("failure!")


#查询某账户已拥有网页列表  输入：账户ID  输出：网页列表
def queryAllPage(request):
    if request.method == "POST":
        user_id = request.POST.get('username')
        result = webpm.queryPage(user_id)
        return HttpResponse(result['content'])



#查询某个已生成的网页  输入：网页ID，账户ID，屏幕分辨率  输出：是否查询成功
def queryPage(request):
    if request.method == "POST":
        user_id = request.POST.get('username')
        page_id = request.POST.get('pageID')
        screen_x = request.POST.get('screenx')
        screen_y = request.POST.get('screeny')
        result = webpm.queryWedget(page_id, user_id)
        if result['status']:
            code = cobu.codeBuilding(result, screen_x, screen_y)
            return HttpResponse(code)
        else:
            return HttpResponse(result['content'])     #打包到前端到最好是json，一个参数判断传的是代码还是失败到信息

