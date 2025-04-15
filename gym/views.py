from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, "gym/index.html")

@login_required
def profile(request):
    user = request.user 
    posts = Costumer.objects.filter(user_c = user)

    return render(request,'gym/profile.html',{'posts':posts})

def post_list(request, category=None):
    if category is not None:
        posts = Costumer.published.filter(category=category)
    else:
        posts = Costumer.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    print(posts, type(posts))
    context = {
        'posts': posts,
        'category': category
    }
    return render(request, "gym/list.html", context)


def post_detail(request, pk):
    post = get_object_or_404(Costumer, id=pk, status=Costumer.Status.PUBLISHED)
#    comments = post.comments.filter(active=True)
#    form = CommentForm()
    context = {
        'post': post,
#        'form': form,
#        'comments': comments,
    }
    return render(request, "gym/detail.html", context)

def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(message=cd['message'], name=cd['name'], email=cd['email'],
                                  phone=cd['phone'], subject=cd['subject'])
            return redirect("gym:profile")
    else:
        form = TicketForm()
    return render(request, "forms/ticket.html", {'form': form})

@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_c = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post= post)
            return redirect('gym:profile')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create-post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Costumer, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('gym:profile')
    return render(request, 'forms/delete-post.html', {'post': post})

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('gym:profile')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Costumer, id=post_id)
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.auser_c = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            return redirect('gym:profile')
    else:
        form = CreatePostForm(instance=post)
    return render(request, 'forms/create-post.html', {'form': form, 'post': post})

# def user_login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('blog:profile')
#                 else:
#                     return HttpResponse('Your account is disabled')
#             else:
#                 return HttpResponse('You are not logged in')
#
#     else:
#         form = LoginForm()
#     return render(request, 'forms/login.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            return  render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_account(request):
#    account = Account(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        account_form = AccountEditForm(request.POST, instance=request.user.account, files=request.FILES)
        if account_form.is_valid() and user_form.is_valid():
            account_form.save()
            user_form.save()
            return redirect('gym:profile')
    else:
        user_form = UserEditForm(instance=request.user)
        account_form = AccountEditForm(instance=request.user.account)   
    context ={
        'account_form': account_form,
        'user_form': user_form
    }
    return render(request, 'registration/edit_account.html', context)