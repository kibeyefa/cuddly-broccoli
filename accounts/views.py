from .forms import LoginFrom, SignupForm 
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import UserProfile


User = get_user_model()
# Create your views here.

def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if 'next' in request.GET:
            redirect = str(request.GET['next'])

    return redirect



def register_view(request):
    user = request.user
    form = SignupForm()
    template_name = 'accounts/signup.html'
    destination = get_redirect_if_exists(request)

    if user.is_authenticated:
        return HttpResponse('You are already logged in...')

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            UserProfile.objects.create(user=user)
            login(request, user)

            return redirect(destination) if destination else redirect('home') 

    return render(request, template_name, {
        'form': form
    })


def login_view(request):
    user = request.user
    form = LoginFrom
    template_name = 'accounts/login.html'
    destination = get_redirect_if_exists(request)
    print(destination)

    if user.is_authenticated:
        return HttpResponse('You are already logged in')

    if request.method == "POST":
        form = LoginFrom(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(destination) if destination else redirect('home')


    return render(request, template_name, {
        'form': form,
    })


def logout_view(request):
    logout(request)
    return redirect('home')


def profile_view(request, username):
    user = request.user
    other_user = User.objects.get(username=username)
    my_self = user == other_user
    profile = UserProfile.objects.get(user=other_user)
    template_name = 'accounts/profile.html'
    print(my_self)
    
    return render(request, template_name, {
        'user': user,
        'other_user': other_user,
        'my_self    ': my_self,
        'profile': profile
    })


@login_required(login_url='accounts:login')
def edit_profile_view(request, username):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    template_name = 'accounts/edit-profile.html'

    if request.method == "POST":
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        print(request.FILES)
        if request.FILES['image']:
            user_profile.image = request.FILES['image']
            user_profile.save()
        user.save()

        return redirect('accounts:profile', username=user.username)

    return render(request, template_name, {
        'user': user,
        'user_profile': user_profile
    })