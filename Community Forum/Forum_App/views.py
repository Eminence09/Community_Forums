from django.shortcuts import render, redirect

from .models import topic_info


def first_page(request):
    if request.method == 'POST':
        topic_name = request.POST.get('topic_names').strip()
        topic_description = request.POST.get('topic_description').strip()
        if topic_name:
            topic_info.objects.create(topic_names=topic_name, topic_description=topic_description)
        return redirect('first_page')

    topics = topic_info.objects.order_by('-id')
    return render(request, 'index.html', {'topics': topics})