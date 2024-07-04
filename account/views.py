from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import LoginForm, UserRegistrationForm, \
    UserEditForm, ProfileEditForm
from .models import Profile


def account_base(request):
    return render(request, 'base_account.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(
                user=new_user,
                photo=user_form.cleaned_data.get('photo'),
                date_of_birth=user_form.cleaned_data.get('date_of_birth')
            )
            return redirect(reverse('register_done', args=[new_user.id]))
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def register_done(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'account/register_done.html', {'new_user': user})


def account_login(request):
    if request.user.is_authenticated:
        return render(request, 'base_account.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'You are logged in successfully.')
                    return redirect(reverse('profile', kwargs={'username': user.username}))
                else:
                    messages.error(request, 'Disabled account')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid login or password')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'account/profile.html', {'user': user})


@login_required
def edit(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect(reverse('profile', kwargs={'username': username}))
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'user': user,
                   'profile_form': profile_form})


@login_required
def account_logout(request):
    logout(request)
    messages.success(request, 'You are logged out of your account.')
    return redirect(reverse('account_menu'))
