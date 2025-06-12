from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth import get_user_model
User = get_user_model()
#mdiddleware kolagi

from .middlewares import auth,guest
# views.py

from .forms import CustomUserCreationForm, CustomAuthenticationForm


# Create your views here.
def nav(request):
    return render(request,'nav.html')
def home(request):
    return render(request,'home.html')

# @guest
# def register_view(request):
#     if request.method=='POST':
#         form=UserCreationForm(request.POST)
#         if form.is_valid():
#             user=form.save()
#             login(request,user)
#             return redirect('login')
#     else:
#         initial_data={'username':'','password1':'','password2':''}
#         form=UserCreationForm(initial=initial_data)
#     return render(request,'register.html',{'form':form})


# @guest
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
            
#             # Check if user is superuser
#             if user.is_superuser:
#                 return redirect('adminpage')  # Your custom admin dashboard URL
#             else:
#                 return redirect('dashboard')  # Regular user dashboard URL
#     else:
#         initial_data={'username':'','password':''}
#         form = AuthenticationForm(initial=initial_data)  # No need for initial data
    
#     return render(request, 'login.html', {'form': form})


@guest
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@guest
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('adminpage')
            else:
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def adminpage(request):
    return render(request,'adminpage.html')




# @guest
# def login_view(request):
#     if request.method=='POST':
#         form=AuthenticationForm(request,data=request.POST)
#         if form.is_valid():
#             user=form.get_user()
#             login(request,user)
#             return redirect('dashboard')
#     else:
#         initial_data={'username':'','password':''}
#         form=AuthenticationForm(initial=initial_data)
#     return render(request,'login.html',{'form':form})

@auth
def dashboard_view(request):
    return render(request,'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def profile(request):
    return render(request,'profile.html')