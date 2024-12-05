from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Car, PurchaseHistory



def registration(request):
    if request.method == 'POST':
       register_form = forms.RegistrationForm(request.POST)
       if register_form.is_valid():
           register_form.save()
           messages.success(request, 'Account Created SuccessFully')
           return redirect('registration')
    else:
        register_form = forms.RegistrationForm()
    return render(request, 'registration.html', {'form': register_form, 'type': 'Registration'})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=name, password=password)  # Checking user in the database
                if user is not None:
                    messages.success(request, 'Logged In Successfully')
                    login(request, user)
                    return redirect('profile')
            else:
                messages.warning(request, 'Login information incorrect, Please try again.')  # For form validation failure
        else:
            form = AuthenticationForm()
        return render(request, 'registration.html', {'form': form, 'type': 'Login'})




def user_logout(request):
    logout(request)
    return redirect('user_login')



@login_required
def user_profile(request):
    data = Car.objects.filter(customer = request.user)
    return render(request, 'profile.html', {'data':data})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile')
    
    else:
        profile_form = forms.ChangeUserForm(instance = request.user)
    return render(request, 'edit_profile.html', {'form' : profile_form})



@login_required
def change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user = request.user, data = request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password Change Successfully')
                update_session_auth_hash(request, form.user)
                return redirect('profile')
        else:
            form = PasswordChangeForm(user = request.user)
        return render(request, 'change_pass.html', {'form':form})
    else:
        return redirect('user_login')
    
@login_required
def buy_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if car.quantity > 0:
        car.quantity -= 1
        car.save()
        
        # Record purchase
        PurchaseHistory.objects.create(user=request.user, car=car)
        messages.success(request, f"You successfully bought the {car.title}!")
    else:
        messages.error(request, f"Sorry, the {car.title} is out of stock.")

    return redirect('order_history') 

@login_required
def order_history(request):
    purchase_history = PurchaseHistory.objects.filter(user=request.user).select_related('car')

    return render(request, 'order_history.html', {'purchase_history': purchase_history})