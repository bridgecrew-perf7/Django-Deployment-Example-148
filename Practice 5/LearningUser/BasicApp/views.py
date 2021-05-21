from django.shortcuts import render
from BasicApp.models import UserProfileInfo
from BasicApp.forms import UserForm, UserProfileInfoForm

from django.urls import reverse
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render (request,"BasicApp/index.html")

def Register(request):

    registered = False
    #Default into have yet to register
    if request.method == "POST":
    # If this is a POST request, we need to get the data into variagbles
        user_form = UserForm(request.POST)
        profile_forms = UserProfileInfoForm(request.POST, request.FILES)
        #Create an instance of the form models and populate it
        if user_form.is_valid() and profile_forms.is_valid():
        #check if validation is successful
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_forms.save(commit=False)
            profile.user = user
            
            profile.save()
            registered = True
            

        else:
            print(user_form.errors, profile_forms.errors)
        return render(request,"BasicApp/register.html",
                {"registered": registered}) 
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        return render(request,"BasicApp/register.html",
                {"registered": registered,
                "user_form":user_form,
                "profile_form":profile_form})    
                
def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'BasicApp/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def specials(request):
    return HttpResponse("You are logged in, NICE")