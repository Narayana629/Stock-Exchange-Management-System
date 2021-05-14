from django.shortcuts import render,redirect
from .models import Registration
from django.contrib.auth.models import auth,User
from django.contrib import messages
# Create your views here.


from Stock.views import overview


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return overview(request)
        else:
            messages.error(request,'Invalid Credintials')
            return redirect('login')


    return render(request,'login/login.html')

def register(request):
    if request.method=="POST":
        print("posting")
        name=request.POST['name']
        uname = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if(password==cpassword):
            if User.objects.filter(username=uname).exists():
                messages.warning(request,'Username already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,'Email already exists')
                return redirect('register')
            else:
                user=User.objects.create_user(username=uname,email=email,password=password,first_name=name)
                user.save()

                messages.success(request, 'Sucessfully Registerd')
                return render(request,'login/login.html')
        else:
            messages.warning(request, 'Passwords are not matching')
            return redirect('register')

    return render(request,'login/register.html')

