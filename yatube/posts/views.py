from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def pgn(post_list, request):
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    post_list = Post.objects.select_related('author').all()
    context = {
        'page_obj': pgn(post_list, request),
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.group.all()
    context = {
        'group': group,
        'page_obj': pgn(post_list, request),
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = User.objects.get(username=username)
    post_list = Post.objects.filter(author=user)
    post_count = Post.objects.filter(author=user).count()
    context = {
        'post_count': post_count,
        'author': user,
        'page_obj': pgn(post_list, request),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = post.author
    post_count = Post.objects.filter(author=user).count()
    context = {
        'post': post,
        'post_count': post_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author)
    return render(request, "posts/create_post.html", {"form": form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST, instance=post)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=pk)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        return redirect('posts:post_detail', post_id=pk)
    return render(request, 'posts/create_post.html',
                  {'form': form, 'is_edit': True})
