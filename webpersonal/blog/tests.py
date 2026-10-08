from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Comment, Post


class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="autor",
            email="autor@example.com",
            password="password123",
        )
        self.staff = get_user_model().objects.create_user(
            username="admin",
            email="admin@example.com",
            password="password123",
            is_staff=True,
        )
        self.post = Post.objects.create(
            title="Entrada de prueba",
            content="Contenido de la prueba.",
            author=self.user,
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Comentario de prueba.",
        )

    def test_blog_home_lists_posts(self):
        response = self.client.get(reverse("blog"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_staff_user_can_delete_comment(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse("delete_comment", args=[self.comment.pk]))

        self.assertRedirects(response, reverse("blog_detail", args=[self.post.slug]))
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())
