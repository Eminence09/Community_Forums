from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import SignUpForm
from .models import topic_info


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('first_page')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('first_page')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('first_page')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('first_page')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required(login_url='login')
def first_page(request):
    import platform
    if request.method == 'POST':
        topic_name = (request.POST.get('topic_names') or '').strip()
        topic_description = (request.POST.get('topic_description') or '').strip()

        if topic_name:
            topic_info.objects.create(
                topic_names=topic_name,
                topic_description=topic_description,
                username=request.user.username,
                # system_name=request.META.get('HTTP_HOST', 'local')
                system_name= platform.node()
            )
        return redirect('first_page')

    topics = topic_info.objects.order_by('-id')
    return render(request, 'index.html', {'topics': topics, 'user': request.user})

