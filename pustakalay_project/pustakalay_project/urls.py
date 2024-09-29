"""
URL configuration for pb_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import login
from django.conf import settings
from django.conf.urls.static import static
from pustakalay_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage, name='home_page'),
    path('login-page/', LoginPage, name='login_page'),
    path('register-page/', RegisterPage, name='register_page'),
    path('forget-password/', ForgetPassword, name='forget_password'),
    path('reset-password/', ResetPassword, name='reset_password'),
    path('profile-page/', ProfilePage, name='profile_page'),
    path('upload-page/', UploadBook, name='upload_page'),
    path('contact-page/', ContactPage, name='contact_page'),
    path('update-user', UpdateUser, name='update_user'),
    path('favourites-page/', FavouritesPage, name='favourites_page'),
    path('add-to-favourite/<str:bookid>/', AddToFavourite, name='add_to_favourite'),
    path('view-book/<str:bookid>/', ViewBook, name='view_book'),
    path('download-book/<str:bookid>/', DownloadBook, name='download_book'),
    path('filter/', Filter, name='filter'),
    path('logout/', Logout, name='logout'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
