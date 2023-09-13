from base64 import urlsafe_b64decode
# import email
# from email.message import EmailMessage
from email import *

# from multiprocessing.context import _force_start_method
# from multiprocessing.sharedctypes import Value
from multiprocessing import *

from telnetlib import LOGOUT
from typing import Type
from datetime import datetime
from pip import main
from .models import ShortLongUrlStore

from django.conf import settings
from django.forms import EmailField, PasswordInput
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage,send_mail

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str

from .tokens import generate_token
from UrlShortner import settings

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello World!")

def home_page(request):
    context = {
            "submitted" : False,
            "keyError" : False
        }
    if request.method == 'POST':
        # print(request.POST)
        data = request.POST #dict
        long_url = data.get('longurl')
        custom_name = data.get('custom_name')
        username = request.user.username
        
        #creating a text file for META data 
        
        # f= open("UserData.txt", 'w')
        # for key, value in request.META.items():
        #     f.write('%s:%s\n' % (key, value))

        # print(request.META)
        # print(long_url)
        # print(custom_name)
        
        try:
            #saving data to data base 
            #create
            obj=ShortLongUrlStore(long_url = long_url,short_url = custom_name,username=username) # table column name <- variable name
            obj.save()
            #read        
            date = obj.date #accessing date from database
            clicks = obj.clicks      
            context['long_url'] = long_url
            context['short_url'] = request.build_absolute_uri() + custom_name
            context['Date'] = date #taken from database
            # context['Date'] = datetime.now().strftime("%B %d, %Y %H : %M") # : %S") #using python
            context['Clicks'] = clicks
            context['submitted'] = True
            if request.user.is_authenticated:
                f_name=request.user.first_name
                context['fname']=f_name
        except:
            context['keyError'] = True
    else:
        print("User not sending any data")
        
    
    # print(request.method)
    return render(request,"index.html",context)

def redirect_url(request,DBreqCustomName):
    filterUrl = ShortLongUrlStore.objects.filter(short_url=DBreqCustomName)
    if len(filterUrl) == 0:
        return HttpResponse("No such short url found.")
    else:
        objFound=filterUrl[0]
        FoundLongUrl = objFound.long_url
        objFound.clicks = objFound.clicks + 1
        objFound.save()
        return redirect(FoundLongUrl)
    
def all_analytics(request):
    user = request.user
    rows = ShortLongUrlStore.objects.filter(username = user)
    context = {
        "rows" : rows
    }
    return render(request, "all-analytics.html",context)

def sign_up(request):
    if request.method == 'POST':
        # print(request.POST)
        data = request.POST #dict
        usernameIn=data.get('username')
        EmailIn = data.get('email')
        fnameIn=data.get('fname')
        lnameIn=data.get('lname')
        PswrdIn = data.get('pswrd')
        ConfirmPswrdIn = data.get('confirmpswrd')
        
        if User.objects.filter(username=usernameIn):
            messages.error(request,"Username already exists...Try another Username")
            return redirect('signup')

        if User.objects.filter(email=EmailIn):
            messages.error(request,"Email already registered...Try another email")
            return redirect('signup')
            
        if len(usernameIn)>10:
            messages.error(request,"Length of Username is > 10")
            return redirect('signup')
        
        if not usernameIn.isalnum():
            messages.error(request,"Only AlphaNumeric values are allowed as Username.")
            return redirect('signup')
        
        try:
            if (PswrdIn == ConfirmPswrdIn):
                myUser=User.objects.create_user(usernameIn,EmailIn,PswrdIn)
                myUser.first_name=fnameIn
                myUser.last_name = lnameIn
                myUser.is_active = True
                # myUser.is_active = False
                myUser.save()
                
                messages.success(request, "Your account is successfully created.Please login with your respective credentials")
                
                """
                EMAIL SECTION
                # messages.success(request, "Your account is successfully created.We have sent you a confirmation mail, plese check your mail box, if not found have a look in spam folder. ")
                
                #Welcome Email
                
                subject = " Welcome to URL Shortner"
                message = "Hola! " + myUser.first_name +"!!\n\n\t Welcome to URL Shortner! A Perfect place to store all your urls in a very easy and accessible way.\n\n  Thank You, for visiting our website!\n\nYou will receive another mail with account activation link, Please click onto that link inorder to activate your account.\n\n Thanking You!\n Darshan Rayala\n URL Shortner Team."
                from_email=settings.EMAIL_HOST_USER
                to_list=[myUser.email]
                send_mail(subject,message, from_email,to_list,fail_silently=True)
                
                # Confirmation Mail
                
                current_site= get_current_site(request)
                email_subject = "Confirm your email @URL Shortner Login"
                message2=render_to_string('email_confirmation.html',
                    {
                    'name':myUser.first_name,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(myUser.pk)),
                    'token':generate_token.make_token(myUser),
                })
                email=EmailMessage(
                    email_subject,
                    message2,settings.EMAIL_HOST_USER,
                    [myUser.email],
                )
                
                email.send()
                email.fail_silently = True
                """
                
                return redirect('signin')
                # return redirect('home')
            else:
                messages.error(request,"Password Mismatch")
        except:
            messages.error(request,"User Already exists...Plese Sign In to continue")
            return redirect('signin')
        
    return render(request,"signUp.html")

def sign_in(request):
    if request.method == 'POST':
        # print(request.POST)
        data = request.POST #dict
        username_emailChk=data.get('username_email')
        PswrdChk = data.get('pswrd')
        
        if '@' in username_emailChk:
            user = authenticate(email=username_emailChk,password=PswrdChk)
        else:
            user = authenticate(username=username_emailChk,password=PswrdChk)

            
        if user is not None:
            login(request,user)
            fname =  user.first_name
            context={
                'fname':fname,
            }
            return redirect('home')
            # return render(request,"index.html",context)
        else:
            messages.error(request,"Bad credentials")
            return redirect('signin')
    return render(request,"signIn.html")


def sign_out(request):
    logout(request)
    messages.success(request,"Successfully Logged out!")
    return redirect('home')


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myUser = User.objects.get(pk=uid)
        
    except(TypeError,ValueError,OverflowError, User.DoesNotExist):
        myUser = None
        
    if myUser is not None and generate_token.check_token(myUser,token):
        myUser.is_active=True
        myUser.save()
        login(request,myUser,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('signin')
    else:
        messages.error(request,"Activation failed try again.")
        return redirect('signup')
    
