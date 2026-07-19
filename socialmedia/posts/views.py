from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required
def home(request):

    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'home.html', {
        'posts': posts
    })


@login_required
def create_post(request):

    if request.method == "POST":

        caption = request.POST.get('caption')
        image = request.FILES.get('image')

        Post.objects.create(
            user=request.user,
            caption=caption,
            image=image
        )

        return redirect('home')

    return render(request, 'create_post.html')
from .models import Post, Like
from django.shortcuts import get_object_or_404
@login_required
def like_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    like = Like.objects.filter(
        user=request.user,
        post=post
    )

    if like.exists():
        like.delete()
    else:
        Like.objects.create(
            user=request.user,
            post=post
        )

    return redirect('home')
from .models import Post, Like, Comment
from django.shortcuts import get_object_or_404

@login_required
def add_comment(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":

        text = request.POST.get("comment")

        if text:
            Comment.objects.create(
                user=request.user,
                post=post,
                comment=text
            )

    return redirect("home")