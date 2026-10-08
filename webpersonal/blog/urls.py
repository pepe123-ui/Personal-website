from django.urls import path

from . import views


urlpatterns = [
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>/like/", views.toggle_post_like, name="toggle_post_like"),
    path("blog/<slug:slug>/", views.blog, name="blog_detail"),
    path(
        "blog/comentario/<int:comment_id>/like/",
        views.toggle_comment_like,
        name="toggle_comment_like",
    ),
    path(
        "blog/comentario/<int:comment_id>/eliminar/",
        views.delete_comment,
        name="delete_comment",
    ),
    path("cuenta/iniciar-sesion/", views.login_view, name="login"),
    path("cuenta/registro/", views.register_view, name="register"),
    path("cuenta/cerrar-sesion/", views.logout_view, name="logout"),
]
