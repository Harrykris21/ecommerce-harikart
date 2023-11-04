from django.shortcuts import render, redirect
from userauths.forms import UserRegistrationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from userauths.models import User

from django.conf import settings

# User = settings.AUTH_USER_MODEL

def register_view(request):

    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, your account was created")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("ecommerceapp:index")
        else:
             print(form.errors)
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }

    return render(request, "userauth/sign-up.html", context)



def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already Logged in")
        return redirect("ecommerceapp:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are loged in")
                return redirect("ecommerceapp:index")    
            else:
                messages.success(request, "User does not exist, Create an account")

        except:
            messages.warning(request, f"User with {email} does not exist")

     

    return render(request, "userauth/login.html")   


def logout_view(request):
    logout(request)
    messages.success(request, "You Logged out")
    return redirect("userauths:sign-in")


