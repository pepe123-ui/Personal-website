from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CommentForm, SignUpForm
from .models import Comment, Post


def blog(request, slug=None):
    if slug:
        post = get_object_or_404(Post.objects.select_related("author"), slug=slug)
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
        comments = post.comments.select_related("author")
        return render(
            request,
            "blog/blog.html",
            {"post": post, "comments": comments, "form": form},
        )

    posts = Post.objects.select_related("author")
    return render(request, "blog/blog.html", {"posts": posts})


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
