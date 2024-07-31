from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Product
from costumerapp.models import Costumer
from .forms import *
from .filters import ProductFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import DetailView
from django.views import View


class Homepage:
    def get(request):
        product_list = Product.objects.all()

        filter_object = ProductFilter(
            data=request.GET,
            queryset=product_list
        )

        context = {'filter_object': filter_object}
        return render(request, 'index.html', context)


def homepage(request):
    product_list = Product.objects.all()

    filter_object = ProductFilter(
        data=request.GET,
        queryset=product_list
    )

    context = {'filter_object':filter_object}
    return render(request, 'index.html', context)


class ProductDetailView(View):
    def get(self, request, pk):
        try:
            product_object = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return HttpResponse('Not found', status=404)
        product_object.views_qty += 1
        if request.user.is_authenticated:
            user = request.user
            if not Costumer.objects.filter(user=user).exists():
                costumer = Costumer.objects.create(
                    name=user.username,
                    age=0,
                    gender='-',
                    user=user,
                )
            costumer = user.costumer
            product_object.costumer_views.add(costumer)
        product_object.save()
        context = {
            "product": product_object,
        }
        return render(request, 'product_detail.html', context)


def product_detail(request, id):
    product_object = Product.objects.get(id=id)

    product_object.views_qty += 1

    if request.user.is_authenticated:
        user = request.user
        if not Costumer.objects.filter(user=user).exists():
            costumer = Costumer.objects.create(
                name=user.username,
                age=0,
                gender='-',
                user=user,
            )
        costumer = user.costumer
        product_object.costumer_views.add(costumer)

    product_object.save()

    context = {
        'product': product_object,
    }
    return render(request, 'product_detail.html', context)


def product_create(request):
    context = {}
    context['product_form'] = ProductForm()

    if request.method == "GET":
        return render(request, 'product_create.html', context)
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            return HttpResponse("Успешно сохранено!")
        return HttpResponse("Ошибка валидации!")


class ProductCreateView(View):
    def get(self, request):
        context = {}
        context["product_form"] = ProductForm()
        return render(request, 'product_create.html', context)

    def post(self, request):
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            return HttpResponse("Успешно сохранено!")
        return HttpResponse("Ошибка валидации!")


class UserCabinet(DetailView):
    model = User
    template_name = 'cabinet.html'  # auth/user_detail.html


# def user_cabinet(request, id):
#     user = User.objects.get(id=id)
#     context = {"user": user}
#     return render(request, 'cabinet.html', context)


def users_list(request):
    user_list = User.objects.all()
    context = {"users": user_list}
    return render(request, 'user_list.html', context)


def search(request):
    keyword = request.GET["keyword"]
    # WHERE name LIKE '%keyword%' OR description LIKE '%keyword%'
    products = Product.objects.filter(
        Q(name__icontains=keyword) |
        Q(description__icontains=keyword)
    )
    context = {"products": products}
    return render(request, 'search_result.html', context)


def profile_create(request):
    context = {}
    context["form"] = ProfileForm()

    if request.method == "GET":
        return render(request, 'profile/create.html', context)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Успешно сохранено!")
        return HttpResponse("Ошибка валидации!")


def profile_update(request, id):
    context = {}
    profile_object = Profile.objects.get(id=id)
    context["form"] = ProfileForm(instance=profile_object)

    if request.method == "GET":
        return render(request, "profile/update.html", context)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile_object)
        if form.is_valid():
            form.save()
            return HttpResponse("Успешно обновлено!")
        return HttpResponse("Ошибка валидации!")


def registration(request):
    context = {}

    if request.method == "POST":
        # create user object
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            user_object = reg_form.save()
            password = request.POST["password"]
            user_object.set_password(password)
            user_object.save()
            return redirect('/')
        return HttpResponse("Ошибка валидации")

    reg_form = RegistrationForm()
    context["reg_form"] = reg_form
    return render(request, 'profile/registration.html', context)


def signin(request):
    context = {}

    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(
                request,
                username=username,
                password=password
            )
            if user is not None:
                login(request, user)
                messages.success(request, "Вы успешно авторизовались!")
                return redirect('/')

            messages.warning(request, "Логин и/или пароль неверны")
        else:
            messages.warning(request, "Данные не валидны")

    form = AuthForm()
    context["form"] = form
    return render(request, 'profile/signin.html', context)


def signout(request):
    logout(request)
    return redirect('/')
