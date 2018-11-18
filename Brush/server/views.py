from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from database.account_management import interfaces as accm


# def index(request):
#     return render(request, 'server/login.html')
# Create your views here.


def home(request):
    # request.Post
    # request.Get
    return render(request, 'home.html')


def login(request):
    # request.Get
    if request.method== 'GET':
        return render(request, 'login.html')
    # request.Post
    if request.method=='POST':
        result = accm.login(request.POST.get('username'),request.POST.get('password'))
        if result['status']:
            response = HttpResponseRedirect('main/')
            response.set_cookie('user_id', request.POST.get('username'))
        else:
            return HttpResponse(result['content'])


def register(request):
    # request.Get
    if request.method=="GET":
        return render(request, 'register.html')
    # request.Post
    if request.method=="POST":
        user_id = request.POST.get('userID_signUp')
        password = request.POST.get('password_signUp')
        result = accm.register(user_id, password)
        if result['status']:
            return HttpResponse(result['content'])
        else:
            return HttpResponse(False)


def menu(request):
    return  render(request, 'menu.html')
