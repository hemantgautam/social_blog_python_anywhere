from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .decorators import logout_require


# Create your views here.
@logout_require
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        # return HttpResponse(form.is_valid())
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # messages.success(request, f'Account created for {username}!')
            messages.success(request, 'Your account has been created. You are ready to login')
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    pr_class = 'active'
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'pr_class': pr_class,
        }
        return render(request, 'users/profile.html', context)


@login_required
def change_password(request):
    pc_class = 'active'
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password successfully updated!')
            return redirect('change_password')
        else:
            # messages.error(request, 'Enter Correct Details')
            return render(request, 'users/profile.html', {'pc_form': form, 'pc_class': pc_class})
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'users/profile.html', {'pc_form': form, 'pc_class': pc_class})