from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category,Post,Comment
from .forms import NewPostForm,NewCommentForm


# Create your views here.

def home(req):
    categories = Category.objects.all()
    user = User.objects.first()
    return render(req, 'categories/home.html', {'categories': categories, 'user': user})


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
    return render(req, 'categories/posts.html',{'category': category})


def new_post(req, category_id):
    category = get_object_or_404(Category, pk=category_id)
    user = User.objects.first()
    if req.method == "POST":
        form = NewPostForm(req.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.category = category
            post.created_by = user
            post.save()
            return redirect('category_posts', category_id=category.pk)
    else:
        form = NewPostForm()

    return render(req, 'categories/new_post.html', {'category': category, 'form': form})


def post(req, category_id, post_id):
    post = get_object_or_404(Post, category__pk=category_id, pk=post_id)
    if req.method == 'POST':
        massage = req.POST['comment']
        created_by = User.objects.first()
        comment = Comment.objects.create(
            massage=massage,
            created_by=created_by,
            post=post
            )
    return render(req, 'categories/post.html', {'post': post})





