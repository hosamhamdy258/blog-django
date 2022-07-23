from traceback import print_tb
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import is_valid_path
from .models import Category, Post, Comment
from .forms import NewPostForm, NewCommentForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage


# Create your views here.

def home(req):
    categories = Category.objects.all()
    posts = Post.objects.all().order_by('-created_dt')
    
    # user = User.objects.first()
    return render(req, 'categories/home.html', {'categories': categories, "posts": posts, "common_tags": common_tags,})


def new_category(req):
    if req.method == 'POST':
        name = req.POST['name']

        category = Category.objects.create(
            name=name
        )
        return redirect('home')
    return render(req, 'categories/new_category.html')


def category_posts(req, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(req, 'categories/posts.html', {'category': category})


# def detail_view(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'categories/detailed.html', {'post': post})
# def tagged(request, slug):
#     tag = get_object_or_404(Tag, slug=slug)
#     posts = Post.objects.filter(tags=tag)
#     context = {
#         'tag':tag,
#         'posts':posts,
#     }
#     return render(request, 'home.html', context)

@login_required
def new_post(req, category_id):
    category = get_object_or_404(Category, pk=category_id)
    # user = User.objects.first()
    common_tags = Post.tags.most_common()[:4]
    if req.method == "POST":
        form = NewPostForm(req.POST)
        print(req.POST)
        if form.is_valid():
            # title and content of post is auto graped and saved by postform
            post = form.save(commit=False)
            # post.slug = slugify(post.title)
            # here added extra data to be saved with post
            post.category = category
            post.created_by = req.user
            # post.image = f"imgs/{req.FILES['image']}"
            # image = req.FILES["image"]
            # fss = FileSystemStorage()
            # fss.save(f"imgs/{image.name}", image)
            post.save()
            form.save_m2m()
            return redirect('category_posts', category_id=category.pk)
    else:
        form = NewPostForm()

    return render(req, 'categories/new_post.html', {'category': category, 'form': form})


@login_required
def post(req, category_id, post_id):
    post = get_object_or_404(Post, category__pk=category_id, pk=post_id)
    if req.method == 'POST':
        form = NewCommentForm(req.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_by = req.user
            comment.post = post
            comment.save()
            return redirect('post', category_id=category_id, post_id=post_id)

    else:
        form = NewCommentForm()

    return render(req, 'categories/post.html', {'post': post, 'form': form})

