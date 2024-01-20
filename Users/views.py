from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout 
from django.contrib.messages import constants
from django.http import HttpResponse





def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        print('a')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password == password_confirm:
            user = User.objects.filter(email=email)
            if not user:
                try:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.add_message(request, constants.SUCCESS, 'Account created successfully')
                    return redirect(reverse('login'))
                except:
                    messages.add_message(request, constants.ERROR, 'Could not create your account')
            else:
                messages.add_message(request, constants.ERROR, 'This email already exists')
        else:
            messages.add_message(request, constants.ERROR, 'Passwords didn\'t match')
        
        return redirect(reverse('signup'))
        
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        
        if user:
            auth_login(request, user)
            return redirect(reverse('novo_flashcard'))
        elif not user:
            messages.add_message(request, constants.ERROR, 'Não foi possível efectuar o login')
            return redirect(reverse('login'))


def logout(request):
    request.session.flush()
    return redirect(reverse('login'))
