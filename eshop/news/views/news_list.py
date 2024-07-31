from django.shortcuts import render
from news.models import New


def news_list(request):
    news_queryset = New.objects.all()  # список объектов
    return render(request, 'news_list.html', {'news': news_queryset})
