from django.shortcuts import render
from django.shortcuts import HttpResponse
from rvr import models

# Create your views here.

#user_list = [
#    {"user":"jack","pwd":"abc"},
#   # {"user":"tom","pwd":"abc"},
#]

def index(request):
    #return HttpResponse('rvr')
    #return render(request, 'index.html',)
    if request.method=="POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        #print(username,password)

        #temp = {"user":username,"pwd":password}
        #user_list.append(temp)

        models.UserInfo.objects.create(user=username, pwd=password)
    user_list = models.UserInfo.objects.all()

    return render(request, "index.html",{"data":user_list})
