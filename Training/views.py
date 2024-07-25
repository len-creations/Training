from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponseRedirect,HttpResponseNotFound
from django.urls import reverse
from .models import User,Profile
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages  
from.forms import profileupdateform,UserProfileForm

# Create your views here.
def index(request):
    return render(request,'Training/layout.html')
def login_view(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            next_url=request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        
        else:
            return render(request,'Training/login.html',{
                "message": "Invalid username and/or password.",
                "next": request.GET.get("next"),
            })
    else:
        return render(request, "Training/login.html", {"next": request.GET.get("next")})
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password=request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Training/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "Training/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Training/register.html")
            
def success_page(request):
    return render(request, 'Training/success.html')
          
@login_required
def update_profile(request):
    try:
        user_instance = request.user
    except AttributeError:
        messages.error(request, 'User object not found. Please log in.')
        return redirect('index')

    if request.method == 'POST':
        form = profileupdateform(request.POST, instance=user_instance)
        if form.is_valid():
            form.save()
            return redirect("success_page")
    else:
        form = profileupdateform(instance=user_instance)

    return render(request, 'Training/create_profile.html', {'form': form})

def custom_404_view(request,exception):
    if "Not Found:" in str(exception):  # Check if the exception message contains "Not Found:"
        return render(request, 'Training/404.html', status=404)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
def Profile_pic(request):
    try:
        user_instance = request.user
        profile_instance, created = Profile.objects.get_or_create(user=user_instance)
    except AttributeError:
        messages.error(request, 'User object not found. Please log in.')
        return redirect('index')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile_instance)
        if form.is_valid():
            form.save()
            return redirect("success_page")
    else:
        form = UserProfileForm(instance=profile_instance)

    return render(request, 'Training/profile_pic.html', {'form': form, 'profile': profile_instance})