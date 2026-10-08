from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count, Exists, OuterRef
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CommentForm, SignUpForm
from .models import Category, Comment, Post


def blog(request, slug=None):
    if slug:
        post = get_object_or_404(
            Post.objects.select_related("author")
            .prefetch_related("categories")
            .annotate(like_count=Count("likes", distinct=True)),
            slug=slug,
        )
        if request.user.is_authenticated:
            post.liked_by_user = post.likes.filter(pk=request.user.pk).exists()
        form = CommentForm()
        if request.method == "POST":
            if not request.user.is_authenticated:
                messages.warning(
                    request, "Tenés que iniciar sesión para comentar."
                )
                return redirect("login")
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, "Comentario publicado.")
                return redirect("blog_detail", slug=post.slug)
        comments = post.comments.select_related("author").annotate(
            like_count=Count("likes", distinct=True)
        )
        if request.user.is_authenticated:
            comments = comments.annotate(
                liked_by_user=Exists(
                    Comment.likes.through.objects.filter(
                        comment_id=OuterRef("pk"),
                        user_id=request.user.pk,
                    )
                )
            )
        return render(
            request,
            "blog/blog.html",
            {"post": post, "comments": comments, "form": form},
        )

    posts = Post.objects.select_related("author").prefetch_related(
        "categories"
    ).annotate(like_count=Count("likes", distinct=True))
    category_slug = request.GET.get("categoria")
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(categories=selected_category)
    return render(
        request,
        "blog/blog.html",
        {
            "posts": posts,
            "categories": Category.objects.all(),
            "selected_category": selected_category,
        },
    )


@require_POST
@login_required(login_url="login")
def toggle_post_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
        messages.success(request, "Like eliminado.")
    else:
        post.likes.add(request.user)
        messages.success(request, "Te gusta esta entrada.")
    return redirect("blog_detail", slug=post.slug)


@require_POST
@login_required(login_url="login")
def toggle_comment_like(request, comment_id):
    comment = get_object_or_404(Comment.objects.select_related("post"), pk=comment_id)
    if comment.likes.filter(pk=request.user.pk).exists():
        comment.likes.remove(request.user)
        messages.success(request, "Like eliminado.")
    else:
        comment.likes.add(request.user)
        messages.success(request, "Te gusta este comentario.")
    return redirect("blog_detail", slug=comment.post.slug)


@require_POST
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    slug = comment.post.slug
    comment.delete()
    messages.success(request, "Comentario eliminado.")
    return redirect("blog_detail", slug=slug)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("blog")
    form = AuthenticationForm(request, data=request.POST or None)
    for field in form.fields.values():
        field.widget.attrs.setdefault("class", "form-control")
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get("next") or request.POST.get("next") or "blog")
    return render(request, "blog/blog.html", {"auth_mode": "login", "form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("blog")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Cuenta creada. ¡Ya podés comentar!")
        return redirect("blog")
    return render(
        request, "blog/blog.html", {"auth_mode": "register", "form": form}
    )


def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect("blog")
