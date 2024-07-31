from django.shortcuts import render, redirect
from news.models import New
from django.contrib import messages


def new_create(request):
    if request.method == "GET":
        return render(request, 'new_create.html')
    elif request.method == "POST":
        # 1. Считывание данные с формы
        data = request.POST
        title = data["new_title"]
        text = data["new_article"]

        # 2. Сохранение этих данных в БД
        new_object = New.objects.create(
            title=title,
            article=text,
        )
        messages.success(request, "Новость успешно добавлена!")
        return redirect(f'/new-detail/{new_object.id}/')

