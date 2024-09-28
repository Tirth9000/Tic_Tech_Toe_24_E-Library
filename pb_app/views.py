from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from .models import *
from .tasks import *
import threading
import random
import string

# Create your views here.
@never_cache
def LoginPage(request):
    if request.method == "POST":
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        
        user = user_authenticate(userid=userid, password=password)
        if user:
            request.session['user_status'] = 'login'
            return redirect('/home')
        else:
            return render(request, "login.html", {"user_invalid" : True})
    return render(request, "login.html")


@never_cache
def RegisterPage(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if LibraryUser.objects.Filter(email=email):
            return render(request, "signup.html", {"error": "Email already exists"})
        else:
            raw_password = request.POST.get('password')
            conf_password = request.POST.get('conf-password')

            if CheckPassword(raw_password):
                return render(request, "signup.html", {"password_invalid": True})
            elif raw_password != conf_password:
                return render(request, "signup.html", {'not_conf_password' : True})
            else:
                random_capital_letters = random.sample(string.ascii_uppercase, 2)
                userid = ''.join(random_capital_letters)
                userid += str(random.randint(1000, 9999))
                while LibraryUser.objects.filter(userid=userid):
                    random_capital_letters = random.sample(string.ascii_uppercase, 2)
                    userid = ''.join(random_capital_letters)
                    userid += str(random.randint(1000, 9999))

                new_user = LibraryUser.objects.Create(
                    userid=userid, 
                    name=request.POST.get('name'), 
                    email=email, 
                    password=set_password(raw_password), 
                    phone=request.POST.get('phone')
                )
                new_user.save()
                ConfirmationMail.delay(new_user.name, new_user.email)
                return redirect('home')
    return render(request, "signup.html")


@never_cache
def ForgetPassword(request):
    if request.method == 'POST':
            if 'email' in request.POST:
                email = request.POST.get('email')
                user = LibraryUser.objects.filter(email=email)

                if user:
                    request.session['user_email'] = email
                    global otp
                    otp = random.randint(100000, 999999)
                    OTPMail.delay(otp, user[0].name, user[0].email)          # Celery applied
                    change_otp_timer = threading.Timer(40.0, ChangeOTP)
                    change_otp_timer.start()
                    return render(request, 'forget.html', {'alert': 'valid', 'otp_send': True, 'email': email})

                else:
                    return render(request, 'forget.html', {'alert': 'invalid', 'email': email})

            elif 'otp' in request.POST:
                get_otp = int(request.POST.get('otp'))
                print("forget",otp)
                try:
                    if otp == get_otp:
                        return redirect('reset_password')
                    else:
                        return render(request, 'forget.html', {'invalid_otp': True})

                except NameError:
                    return render(request, 'forget.html', {'invalid_otp': True})
                
    return render(request, 'forget.html')


@never_cache
def ResetPassword(request):
    if request.method == "POST":
        password = request.POST.get('new-password')
        confirmPassword = request.POST.get('confirm-password')
        if CheckPassword(password):
            return render(request, 'reset.html', {'invalid_password': True})

        elif password != confirmPassword:
            return render(request, 'reset.html', {'confirm_password': True})

        else:
            get_user = LibraryUser.objects.get(email=request.session.get('user_email'))
            get_user.password = set_password(password)
            get_user.save()
            request.session.pop('user_email', None)
            return redirect('login')
    return render(request, 'reset.html')


@never_cache
def HomePage(request):
    books = Books.objects.all()
    return render(request, "home.html", {'books': books})
    return render(request, "home.html")


def ProfilePage(request):
    return render(request, "profile.html")

def UploadPage(request):
    return render(request, "upload.html")


def ChangeOTP():
    global otp
    otp = 0