from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django_htmx.http import trigger_client_event
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseForbidden

from blog.forms import LoginForm, RegisterForm,BlogForm,AuthorSelectForm,UserForm,AuthorSelectForm,UserProfileForm
from blog.models import User,Blog

def main(request):
    login = request.session.get("authorized_user_login", None)
    users = User.objects.all()
    return render(request, 'base.html', {'login': login, 'users': users})


def login_frame(request, error=""):
    login = request.session.get("authorized_user_login", None)

    return render(
        request,
        "login_logout_frame.html",
        {"login_form": LoginForm(), "user_login": login, "login_error": error},
    )


def register_frame(request):
    login = request.session.get("authorized_user_login", None)
    return render(request, "register_frame.html", {"user_login": login})

def register_form_frame(request, registered_ok=False, reg_error=""):
    return render(
        request,
        "register_form_frame.html",
        {
            "registered_ok": registered_ok,
            "reg_error": reg_error,
            "register_form": RegisterForm(),
        },
    )


def register_User_data(f):
    if not f.is_valid():
        raise RuntimeError("Error: " + str(f.errors))

    login = f.cleaned_data["reg_login"]
    name = f.cleaned_data["name"]
    password = f.cleaned_data["reg_password"]
    passagain = f.cleaned_data["passagain"]

    if len(User.objects.filter(login=login)) > 0:
        raise RuntimeError(f"A User with the login {login} already exists.")

    if password != passagain:
        raise RuntimeError("Passwords do not match.")

    User.objects.create(
        name=name, 
        login=login, 
        password=make_password(password),
        icon='default_icon.png',
        profile='よろしくお願いします。'
    )
    return login


def do_register(request):
    reg_error = None
    f = RegisterForm(request.POST)
    evt = ""

    try:
        login = register_User_data(f)
        evt = "evt_login"
        do_login_user(request, login)

    except RuntimeError as e:
        reg_error = str(e)

    response = register_form_frame(request, reg_error is None, reg_error)
    return trigger_client_event(response, evt)

def do_check_regform(request):
    f = RegisterForm(request.POST)
    r = ""

    p = User.objects.filter(login=f.data["reg_login"])
    if len(p) != 0:
        r = "Login already used!"

    if f.data["reg_password"] != f.data["passagain"]:
        r = "Passwords don't match!"

    return HttpResponse(r)


def do_login_user(request, login):
    request.session["authorized_user_login"] = login


def do_login(request):
    f = LoginForm(request.POST)
    error = ""
    evt = ""
    try:
        if not f.is_valid():
            raise RuntimeError()

        p = User.objects.filter(login=f.cleaned_data["login"])
        if len(p) == 0 or not check_password(f.cleaned_data["password"], p[0].password):
            raise RuntimeError()

        do_login_user(request, p[0].login)
        evt = "evt_login"

    except RuntimeError:
        error = "Wrong username or password."

    return trigger_client_event(login_frame(request, error), evt)


def load_login_logout_frame(request):
    return render(request, "test-form.html", {"counter": None})


def do_logout(request):
    request.session["authorized_user_login"] = None
    return trigger_client_event(login_frame(request), "evt_login")

def hello(request):
    login = request.session.get("authorized_user_login", None)
    return render(request, "hello.html", {"user_login": login})

def create_blog_view(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            login = request.session.get("authorized_user_login", None)
            if login:
                user = User.objects.get(login=login)
                blog.author = user
            else:
                default_user = User.objects.first()
                blog.author = default_user
            blog.save()
            return redirect("home")
    else:
        form = BlogForm()

    login = request.session.get("authorized_user_login", None)
    return render(request, 'create_blog.html', {'form': form, 'user_login': login})

def blog_list_view(request):
    authors = User.objects.all()
    form = AuthorSelectForm(request.GET, authors=authors)
    author_name = request.GET.get('author')
    date = request.GET.get('date')
    keyword = request.GET.get('keyword')

    blog_list = Blog.objects.all()

    if author_name:
        author = get_object_or_404(User, name=author_name)
        blog_list = blog_list.filter(author=author)

    if date:
        blog_list = blog_list.filter(timeslot__date=date)

    if keyword:
        blog_list = blog_list.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))

    blog_list = blog_list.order_by('-timeslot')

    paginator = Paginator(blog_list, 10)
    page_number = request.GET.get('page', 1)
    try:
        page_number = int(page_number)
    except (ValueError, TypeError):
        page_number = 1

    page_obj = paginator.get_page(page_number)

    return render(request, 'blog_list.html', {'page_obj': page_obj, 'form': form})

def user_icon(request):
    user_login = request.session.get("authorized_user_login", None)
    if user_login:
        user = User.objects.get(login=user_login)
        return render(request, 'user_icon.html', {'user': user, 'user_login': user_login})
    return render(request, 'user_icon.html', {'user_login': None})

def create_button(request):
    user_login = request.session.get("authorized_user_login", None)
    context = {
        'user_login': user_login
    }
    return render(request, 'create_button.html', context)

def author_blog_list_view(request, author_name):
    author = get_object_or_404(User, name=author_name)
    blog_list = Blog.objects.filter(author=author).order_by('-timeslot')
    paginator = Paginator(blog_list, 10)

    page_number = request.GET.get('page', 1)
    try:
        page_number = int(page_number)
    except (ValueError, TypeError):
        page_number = 1
    
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog_list.html', {'page_obj': page_obj, 'author': author})

def register_userdata(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.icon = form.cleaned_data['icon']
            user.save()
            request.session['authorized_user_login'] = user.login
            return redirect('/home')
    else:
        form = UserForm()
    return render(request, 'register_userdata.html', {'form': form})

def delete_blogs_view(request):
    login = request.session.get("authorized_user_login", None)
    user = User.objects.get(login=login)
    blogs = Blog.objects.filter(author=user)
    return render(request, 'delete_blogs.html', {'blogs': blogs})

def delete_selected_blogs(request):
    login = request.session.get("authorized_user_login", None)
    if request.method == 'POST':
        blog_ids = request.POST.getlist('selected_blogs')
        Blog.objects.filter(id__in=blog_ids, author=User.objects.get(login=login)).delete()
    return redirect('/home')

def delete_button(request):
    user_login = request.session.get("authorized_user_login", None)
    context = {
        'user_login': user_login
    }
    return render(request, 'delete_button.html', context)

def user_profile_view(request):
    login = request.session.get("authorized_user_login", None)
    user = User.objects.get(login=login)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'user_profile.html', {'form': form})

def user_profile_button(request):
    user_login = request.session.get("authorized_user_login", None)
    context = {
        'user_login': user_login
    }
    return render(request, 'user_profile_button.html', context)