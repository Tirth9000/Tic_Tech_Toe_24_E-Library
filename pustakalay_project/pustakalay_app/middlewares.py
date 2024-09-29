from django.shortcuts import render, redirect

def Authorised_user(request_function):
    def inner_function(request, *args, **kwargs):
        if request.session.get('user_status') != 'login':
            return redirect('home_page')
        return request_function(request, *args, **kwargs)
    return inner_function 

def download_permission(reqeust_function):
    def inner_function(request, *args, **kwargs):
        if request.session.get('login') != 1:
            return redirect('home_page')
        return reqeust_function(request, *args, **kwargs)
    return inner_function
