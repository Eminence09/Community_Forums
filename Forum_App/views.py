from django.shortcuts import render

def first_page(requests):
    return render(requests, 'index.html')
