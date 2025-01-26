from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings as conf_settings
from .models import Store, Medicine
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
import random
import string
from django.core.mail import send_mail
from .models import Profile

# Home page view
def home(request):
    return render(request, 'website/home.html')

# Other existing views (like about, service, etc.)
def about(request):
    return render(request, 'website/about.html')

def service(request):
    return render(request, 'website/service.html')

def pricing(request):
    return render(request, 'website/pricing.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user instance
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()

            # Save additional profile information, such as role (Volunteer or Business Owner)
            role = form.cleaned_data['role']
            profile = Profile(user=user, role=role)  # Assuming you have a Profile model to store this
            profile.save()

            messages.success(request, "Registered successfully!")
            return redirect('login')  # Redirect to the login page after successful registration
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()

    return render(request, 'website/signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have logged in successfully!")
                # Redirect to the profile page showing user's name
                return redirect('profile')  # This will now redirect to the profile page
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AuthenticationForm()

    return render(request, 'website/login.html', {'form': form})

# Profile page showing user's name
@login_required
def profile_view(request):
    # Fetching the logged-in user's name
    user_name = request.user.username
    return render(request, 'website/afterlogin/home.html', {'user_name': user_name})

# Ensure the home page is only accessible after login
# @login_required
# def after_login_home(request):
#     return render(request, 'website/afterlogin/home.html')

# After Login
def newhome(request):
    return render(request, 'website/afterlogin/home.html') # This will be the home page after login

def awareness(request):
    return render(request, 'website/afterlogin/awareness.html')

def newcontact(request):
    return render(request, 'website/afterlogin/contact.html')

# Blog View
def blog(request):
    return render(request, 'website/blog.html')

# Blog details View
def blog_details(request):
    return render(request, 'website/blog_details.html')

# Catalogue View
def catalogue(request):
    return render(request, 'website/catalogue.html')

# Contact View
def contact(request):
    if request.method == 'POST':
        name = request.POST['message_name']
        email = request.POST['message_email']
        message = request.POST['message']
        
        # Send email to the default address
        send_mail(
            'Follow up required for - ' + name,
            message,
            email,
            [conf_settings.CONTACT_US_FORM_EMAIL_TO],
            fail_silently=False,
        )

        messages.success(request, f'Hi {name}, Thanks for contacting us. We will follow up with you within the next few business days.')
        return redirect('contact')
    else:
        return render(request, 'website/contact.html')

# Store View
def store(request):
    stores = Store.objects.all()
    return render(request, 'website/store.html', {'stores': stores})

# Genstores View
def genstores(request):
    stores = Store.objects.all()
    return render(request, 'website/genstores.html', {'stores': stores})

# Get Districts API
def get_districts(request):
    state = request.GET.get('state')
    districts = Store.objects.filter(store_state=state).values_list('store_district', flat=True).distinct()
    return JsonResponse({'districts': list(districts)})

# Get Stores API
def get_stores(request):
    state = request.GET.get('state')
    district = request.GET.get('district')
    if state and district:
        stores = Store.objects.filter(
            store_state=state, 
            store_district=district
        ).values(
            'store_code', 
            'store_state', 
            'store_district', 
            'store_address', 
            'store_pincode', 
            'store_contact'
        )
        return JsonResponse({'stores': list(stores)})
    
    return JsonResponse({'stores': []})

# Medicine Search API
@csrf_protect
def search_medicines(request):
    if request.method == 'POST':
        search_query = request.POST.get('search', '')
        medicines = Medicine.objects.filter(name__icontains=search_query)

        # Prepare the response
        results = []
        for med in medicines:
            results.append({
                'name': med.name,
                'price': med.price,
                'description': med.description,
                'image': med.image.url if med.image else '/path/to/default/image.jpg'  # Fallback if no image
            })

        return JsonResponse({'medicines': results})

