from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SignUpForm
from .models import TopicReply, topic_info
import datetime

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


def documentation(request):
    documentation_sections = [
        {
            'title': 'Start here',
            'description': 'Get a project running and understand the pieces that make up a Django application.',
            'documents': [
                {
                    'title': 'Django overview',
                    'description': 'A high-level introduction to Django and its core concepts.',
                    'url': 'https://docs.djangoproject.com/en/5.0/intro/overview/',
                    'label': 'Beginner',
                },
                {
                    'title': 'Writing your first Django app',
                    'description': 'Build a small application from models through views and templates.',
                    'url': 'https://docs.djangoproject.com/en/5.0/intro/tutorial01/',
                    'label': 'Tutorial',
                },
                {
                    'title': 'Django installation guide',
                    'description': 'Install Django and choose the right setup for your operating system.',
                    'url': 'https://docs.djangoproject.com/en/5.0/topics/install/',
                    'label': 'Setup',
                },
            ],
        },
        {
            'title': 'Build with Django',
            'description': 'Find the reference material for the parts you use every day.',
            'documents': [
                {
                    'title': 'Models and databases',
                    'description': 'Define data models, relationships, migrations, and database queries.',
                    'url': 'https://docs.djangoproject.com/en/5.0/topics/db/',
                    'label': 'Data',
                },
                {
                    'title': 'Views and URL routing',
                    'description': 'Connect URLs to views and return the right response for each request.',
                    'url': 'https://docs.djangoproject.com/en/5.0/topics/http/urls/',
                    'label': 'Web',
                },
                {
                    'title': 'Templates',
                    'description': 'Render dynamic pages with Django\'s template language.',
                    'url': 'https://docs.djangoproject.com/en/5.0/topics/templates/',
                    'label': 'Frontend',
                },
                {
                    'title': 'Forms',
                    'description': 'Create, validate, and process forms safely.',
                    'url': 'https://docs.djangoproject.com/en/5.0/topics/forms/',
                    'label': 'Forms',
                },
            ],
        },
        {
            'title': 'Solve common problems',
            'description': 'Practical references for authentication, files, and testing.',
            'documents': [
                {
                    'title': 'Authentication and authorization',
                    'description': 'Work with users, sessions, login, logout, and permissions.',
                    'url': 'https://docs.djangoproject.com/en/5.0/topics/auth/',
                    'label': 'Users',
                },
                {
                    'title': 'Testing in Django',
                    'description': 'Write tests for views, models, forms, and complete workflows.',
                    'url': 'https://docs.djangoproject.com/en/5.0/topics/testing/',
                    'label': 'Testing',
                },
                {
                    'title': 'Static files',
                    'description': 'Manage CSS, JavaScript, images, and collected assets.',
                    'url': 'https://docs.djangoproject.com/en/5.0/howto/static-files/',
                    'label': 'Assets',
                },
            ],
        },
        {
            'title': 'Ship with confidence',
            'description': 'Prepare a project for production and keep it secure.',
            'documents': [
                {
                    'title': 'Deployment checklist',
                    'description': 'Review security, performance, and configuration before launch.',
                    'url': 'https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/',
                    'label': 'Production',
                },
                {
                    'title': 'Security in Django',
                    'description': 'Learn how Django helps protect applications and where to take care.',
                    'url': 'https://docs.djangoproject.com/en/5.0/topics/security/',
                    'label': 'Security',
                },
                {
                    'title': 'Django API reference',
                    'description': 'Look up the complete reference for Django\'s built-in APIs.',
                    'url': 'https://docs.djangoproject.com/en/5.0/ref/',
                    'label': 'Reference',
                },
            ],
        },
    ]
    document_count = sum(len(section['documents']) for section in documentation_sections)
    return render(request, 'documentation.html', {
        'documentation_sections': documentation_sections,
        'document_count': document_count,
    })


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
                # uploaded_datetime = datetime.datetime.now(),
                # system_name=request.META.get('HTTP_HOST', 'local')
                system_name= platform.node()
            )
        return redirect('first_page')

    topics = topic_info.objects.order_by('-id')
    return render(request, 'index.html', {'topics': topics, 'user': request.user})


@login_required(login_url='login')
def new_announcements(request):
    topics = topic_info.objects.order_by('-id')
    return render(request, 'new_announcements.html', {'topics': topics, 'user': request.user})


@login_required(login_url='login')
def topic_detail(request, topic_id):
    topic = get_object_or_404(topic_info, id=topic_id)

    if request.method == 'POST':
        reply_body = (request.POST.get('body') or '').strip()
        if reply_body:
            TopicReply.objects.create(
                topic=topic,
                username=request.user.username,
                body=reply_body,
            )
        return redirect('topic_detail', topic_id=topic.id)

    return render(request, 'topic_detail.html', {
        'topic': topic,
        'replies': topic.replies.all(),
        'user': request.user,
    })