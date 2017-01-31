from django.http import HttpResponse, HttpResponseRedirect
#from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import (LoginForm, UserRegistrationForm,
                    ProfileRegistrationForm, feedbackForm,
                    ProfileEditForm)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone

#import win32api

EMAIL_HOST_USER = 'ron2tele@gmail.com'
TOTAL_PH_TIME = 6 # It is in hours

# for validation
def startsWithNumber(value):
    for i in range(10):
        if value.startswith(str(i)):
            return True
    return False

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
            else:
                return HttpResponse('Disabled account')
            
        else:
            return HttpResponse('Invalid login')

    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})

def register(request):
    registered = False
    errors = []
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileEditForm(request.POST)
        
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            #new_user_profile = profile_form.save(commit=False)
         
            # Set the chosen fields
            user_form.cleaned_data['username']
            new_user.set_password(user_form.cleaned_data['password'])

            first_name = request.POST['first_name']
            surname = request.POST['surname']
            account_number = request.POST['account_number']
            phone = request.POST['phone']
            
            if len(first_name) < 3 or len(first_name) > 25:
                errors.append(
                    'First name must be between 3 and 25 characters long')
            elif not first_name.isalpha():
                errors.append(
                    'First name must contain only alphabets')

            if len(surname) < 3 or len(surname) > 25:
                errors.append(
                    'Surname must be between 3 and 25 characters long')
            elif not surname.isalpha():
                errors.append(
                    'Surname must contain only alphabets')

            if len(account_number) != 10:
                errors.append('Invalid account number')
            elif not account_number.isdigit():
                errors.append(
                    'Account number must contain only digits')

            if len(phone) != 11:
                errors.append('Invalid phone number')
            elif not phone.isdigit():
                errors.append('Phone number must contain only digits')
                
            """
            new_user_profile.first_name = profile_form.cleaned_data['first_name']
            new_user_profile.surname = profile_form.cleaned_data['surname']
            new_user_profile.phone = profile_form.cleaned_data['phone']
            new_user_profile.bank = profile_form.cleaned_data['bank']
            new_user_profile.account_number = profile_form.cleaned_data['account_number']
            """
            if not errors:
                # Save the User object
                new_user.save()

                # Create the user profile
                profile = Profile.objects.create(user=new_user)
                profile.first_name = first_name
                profile.surname = surname
                profile.phone = phone
                profile.bank = request.POST['bank']
                profile.account_number = account_number
                profile.save()
                
                # Set registered True
                registered = True

                # Reset the form to default
                user_form = UserRegistrationForm()
                profile_form = ProfileEditForm()
                
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileEditForm()
        
    return render(request, 'account/register.html',
                          {'errors': errors,
                           'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})

def home(request):
    if request.user.is_authenticated():
        # Redirect to dashboard if user is logged in
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
                        
    return render(request, 'account/home.html')

"""
def feedback(request):
    if request.method == 'POST':
        # Form was submitted
        form = feedbackForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            send_mail(cd['subject'], cd['message'], cd['email'], ['ProtonPayer@Protonmail.com'])
            sent = True
    else:
        form = feedbackForm()

    return render(request, 'account/feedback.html', {'form': form,
                                                    'sent': sent})
"""

@login_required
def dashboard(request):
    # Add initial PH details
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user)

    time_left = int(TOTAL_PH_TIME*3600 - (
            timezone.now() - profile.PH_time).total_seconds())

    if profile.deactivated:
        pass
    elif profile.matched == True and profile.PHed == False:
        profile.deactivated = True if time_left <= 0 else False
        profile.save()

        if profile.deactivated:
            GHer = profile.upliner.all()[0]
            pfile = Profile.objects.get(user=GHer)
            pfile.downliner.remove(user) ##################
            pfile.no_of_payers -= 1
            pfile.save()
    
    return render(request, 'account/dashboard.html')

@login_required
def transactions(request):
    # Add initial PH details
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user)

    time_left = int(TOTAL_PH_TIME*3600 - (
            timezone.now() - profile.PH_time).total_seconds())

    if profile.deactivated:
        # Redirect to dashboard if user is logged in
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    
    elif profile.matched == True and profile.PHed == False:
        profile.deactivated = True if time_left <= 0 else False
        profile.save()
        
        if profile.deactivated:
            GHer = profile.upliner.all()[0]
            pfile = Profile.objects.get(user=GHer)
            pfile.downliner.remove(user) ##################
            pfile.no_of_payers -= 1
            pfile.save()
            
            # Redirect to dashboard if user is logged in
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


    # POST request
    if request.method == 'POST':
        # For new user
        if profile.package == "None":
            profile.matched = False
            profile.package = str(request.POST['amt'])
            profile.PH_time = timezone.now()
            profile.PHed = False
            profile.no_of_payers = 0

            # Save edited  profile details
            profile.save()

        else:
            # For GHer confirmation
            usr = User.objects.get(username=request.POST["user"])
            pfile = Profile.objects.get(user=usr)

            time_left = int(TOTAL_PH_TIME*3600 - (
                        timezone.now() - pfile.PH_time).total_seconds())

            pfile.deactivated = True if time_left <= 0 else False
            pfile.save()

            if pfile.deactivated:
                profile.downliner.remove(pfile.user) ##################
                profile.no_of_payers -= 1
                profile.save()

            else:                      
                # set PHer info
                pfile.matched = True
                pfile.PHed = True
                pfile.PH_time = timezone.now()
                pfile.no_of_payers = 0
                pfile.no_of_paid = 0
                pfile.upliner.remove(user)
                pfile.save()
                    
                # set GHer info
                profile.downliner.remove(usr)
                profile.no_of_paid += 1
                profile.save()
                
                # Reset GHer if payment is completed
                if profile.no_of_paid == 2:
                    profile.matched = False
                    profile.package = "None"
                    profile.PHed = False
                    profile.PH_time = timezone.now()
                    profile.no_of_payers = 0
                    profile.no_of_paid = 0

                    d_list = profile.downliner.all()
                    for i in range(len(d_list)):
                        profile.downliner.remove(d_list[i])
                        
                    profile.save()
     

    ###################################
    # Auto matching
    ###################################

    # For assigning a new user to a GHer
    if profile.package != "None": # None is for Reseted GHers
        if profile.matched == False:
            GH_list = Profile.GH_list.filter(package=profile.package)
            GH_list = GH_list.order_by('PH_time') ############ Check Here

            for them in GH_list:
                if them.no_of_payers < 2 and not user in them.downliner.all():
                    # For the GHer
                    them.no_of_payers += 1
                    them.downliner.add(user)

                    # For the PHer
                    profile.PH_time = timezone.now()
                    profile.matched = True
                    profile.upliner.add(them.user)

                    # Save edited  profile details
                    profile.save()
                    them.save()
                    
                    break

        elif profile.matched and profile.PHed: # A GHer
            if profile.no_of_payers < 2:
                PH_list = Profile.PH_list.filter(package=profile.package)
                PH_list = PH_list.order_by('PH_time')

                count = 0
                while profile.no_of_payers < 2 and count < len(PH_list):
                    if not PH_list[count].user in profile.downliner.all():
                        profile.no_of_payers += 1
                        profile.downliner.add(PH_list[count].user)
                        
                        PH_list[count].PH_time = timezone.now()
                        PH_list[count].matched = True
                        PH_list[count].upliner.add(user)

                        # Save edited  profile details
                        profile.save()
                        PH_list[count].save()
                        
    
    GH_user = None
    GH_profile = None
    init_time = None
    PHer_profile_list = []

    if profile.package != "None":
        # Handles PHer 
        if profile.matched and not profile.PHed:
            GH_user = profile.upliner.all()[0]
            GH_profile = Profile.objects.get(user=GH_user)

            time_left = int(TOTAL_PH_TIME*3600 - (
                timezone.now() - profile.PH_time).total_seconds())
            
            init_time = str(time_left)

        # Handles GHer 
        elif profile.matched and profile.PHed:
            GH_user = user
            GH_profile = profile
            init_time = []
            d_list = profile.downliner.all()

            if len(d_list) > 0: # Check if time of downliners has expired
                for i in range(len(d_list)):
                    pfile = Profile.objects.get(user=d_list[i])
                    time_left = int(TOTAL_PH_TIME*3600 - (
                        timezone.now() - pfile.PH_time).total_seconds())

                    pfile.deactivated = True if time_left <= 0 else False
                    pfile.save()

                    if pfile.deactivated:
                        profile.downliner.remove(pfile.user) ##################
                        profile.no_of_payers -= 1
                        profile.save()

            d_list = profile.downliner.all()
            for i in range(len(d_list)):
                pfile = Profile.objects.get(user=d_list[i])
                PHer_profile_list.append(pfile)

                time_left = int(TOTAL_PH_TIME*3600 - (
                    timezone.now() - pfile.PH_time).total_seconds())
            
                pfile.init_time = str(time_left)
                pfile.save()
                
    return render(request, 'account/send_cash.html', {'GH_user': GH_user,
                                                      'GH_profile': GH_profile,
                                                      'PH_user': profile,
                                                      'PHer_profile_list': PHer_profile_list,
                                                      'init_time': init_time})

@login_required
def profile(request):
    updated = False
    errors = []
    if request.method == 'POST':
        profile_form = ProfileEditForm(instance=request.user.profile,
                                               data=request.POST)

        if profile_form.is_valid():
            first_name = request.POST['first_name']
            surname = request.POST['surname']
            account_number = request.POST['account_number']
            phone = request.POST['phone']
            
            if len(first_name) < 3 or len(first_name) > 25:
                errors.append(
                    'First name must be between 3 and 25 characters long')
            elif not first_name.isalpha():
                errors.append(
                    'First name must contain only alphabets')

            if len(surname) < 3 or len(surname) > 25:
                errors.append(
                    'Surname must be between 3 and 25 characters long')
            elif not surname.isalpha():
                errors.append(
                    'Surname must contain only alphabets')

            if len(account_number) != 10:
                errors.append('Invalid account number')
            elif not account_number.isdigit():
                errors.append(
                    'Account number must contain only digits')

            if len(phone) != 11:
                errors.append('Invalid phone number')
            elif not phone.isdigit():
                errors.append('Phone number must contain only digits')
        
            if not errors:
                profile_form.save()
                updated = True

    else:
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/profile.html', {'section': 'profile',
                                                    'updated': updated,
                                                    'errors': errors})

