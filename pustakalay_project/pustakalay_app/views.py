from django.shortcuts import render, redirect
from django.http import FileResponse, Http404, HttpResponse
from django.views.decorators.cache import never_cache

import os
from pustakalay_project import settings
from .models import *
from .tasks import *
from .middlewares import *
import threading
import random
import string

# Create your views here.
@never_cache
def LoginPage(request):
    if request.method == "POST":
        useremail = request.POST.get('email')
        password = request.POST.get('password')
        
        user = user_authenticate(useremail=useremail, password=password)
        if user:
            request.session['user_status'] = 'login'
            request.session['userid'] = user.userid
            request.session['login'] = 1
            books = Books.objects.all()
            return render(request, 'home.html', {'user': user, 'userlogin': request.session.get('login'), 'books': books})
        else:
            return render(request, "login.html", {"user_invalid" : True})
    return render(request, "login.html")


@never_cache
def RegisterPage(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if LibraryUser.objects.filter(email=email):
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

                new_user = LibraryUser.objects.create(
                    userid=userid, 
                    username=request.POST.get('name'), 
                    email=email, 
                    password=set_password(raw_password), 
                    phone=request.POST.get('phone')
                )
                ConfirmationMail.delay(new_user.username, new_user.email)
                new_user.save()
                return redirect('home_page')
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
                    OTPMail.delay(otp, user[0].username, user[0].email)          # Celery applied
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
    return render(request, "home.html", {'userlogin': request.session.get('login'), 'books': books})


@Authorised_user
@never_cache
def ProfilePage(request):
    userid = request.session.get('userid')
    user = LibraryUser.objects.get(userid=userid)
    user_books = Books.objects.filter(userid=user)
    return render(request, "profile.html", {'userlogin': request.session.get('login'), 'user': user, 'books': user_books})

@Authorised_user
def UploadBook(request):
    if request.method == "POST":
        userid = request.session.get('userid')
        user = LibraryUser.objects.get(userid=userid)
        fileID = random.randint(100000, 999999)

        new_data = Books.objects.create(
            userid = user,
            fileID = fileID,
            book_title = request.POST.get('title'),
            bookDescription = request.POST.get('description'),
            author = request.POST.get('author'),
            publish = request.POST.get('publish'),
            category = request.POST.get('category')
        )
        if request.FILES.get('cover') is not None:
            new_data.book_photo = request.FILES.get('cover')
        if request.FILES.get('book-file') is not None:
            new_data.book_pdf = request.FILES.get('book-file')
        new_data.save()
    return render(request, "upload.html", {'userlogin': request.session.get('login')})


def Logout(request):
    request.session.pop('user_status', None)
    request.session.pop('userid', None)
    request.session['login'] = 0
    return redirect('home_page')
    return render(request, 'home.html', {'userlogin': 0})

# @Authorised_user
def ContactPage(request):
    return render(request, "contact.html")


@Authorised_user
@never_cache
def UpdateUser(request):
    user = LibraryUser.objects.get(userid = request.session.get('userid'))
    if request.method == 'POST':
        user.username = request.POST.get('name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        if request.FILES.get('profile-pic') is not None:
            user.photo = request.FILES.get('profile-pic')
        user.save()
        return redirect('profile_page')
    return render(request, 'update.html', {'user': user})


@Authorised_user
def FavouritesPage(request):
    userid = request.session.get('userid')
    user = LibraryUser.objects.get(userid = userid)
    print(user)
    book = FavouritiesBooks.objects.filter(user = user)
    print(book)
    return render(request, 'my_fav.html', {'books': book})


def ViewBook(request, bookid):
    try:
        book = Books.objects.get(fileID = bookid)
    except Books.DoesNotExist:
        book = None
        return HttpResponse("Book doesn't exist")
    return render(request, 'product.html', {'book': book, 'userlogin': request.session.get('login')})


@Authorised_user
def AddToFavourite(request, bookid):
    userid = request.session.get('userid')
    book = Books.objects.get(fileID = bookid)
    new_favourite = FavouritiesBooks.objects.create(
        user = LibraryUser.objects.get(userid = userid),
        book = book
    )
    new_favourite.save()
    return render(request, 'product.html', {'addToFav' : True})

@download_permission
def DownloadBook(request, bookid):
    book = Books.objects.get(fileID = bookid)
    file_path = os.path.join(settings.MEDIA_ROOT, book.book_pdf.name)
    try:
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404("PDF file not found")


def Filter(request):
    if request.method == 'GET':
        selected_categories = request.GET.getlist('category')
        books = Books.objects.filter(category = selected_categories)
    return render(request, 'home.html', {'books': books})
    




def ChangeOTP():
    global otp
    otp = 0
