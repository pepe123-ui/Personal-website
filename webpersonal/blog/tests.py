from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Comment, Post


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

    def test_authenticated_user_can_toggle_post_like(self):
        self.client.force_login(self.user)
        url = reverse("toggle_post_like", args=[self.post.slug])

        response = self.client.post(url)

        self.assertRedirects(response, reverse("blog_detail", args=[self.post.slug]))
        self.assertEqual(self.post.likes.count(), 1)

        self.client.post(url)
        self.assertEqual(self.post.likes.count(), 0)

    def test_authenticated_user_can_toggle_comment_like(self):
        self.client.force_login(self.user)
        url = reverse("toggle_comment_like", args=[self.comment.pk])

        response = self.client.post(url)

        self.assertRedirects(response, reverse("blog_detail", args=[self.post.slug]))
        self.assertEqual(self.comment.likes.count(), 1)

        self.client.post(url)
        self.assertEqual(self.comment.likes.count(), 0)

    def test_anonymous_user_cannot_like(self):
        response = self.client.post(
            reverse("toggle_post_like", args=[self.post.slug])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
        self.assertEqual(self.post.likes.count(), 0)

    def test_category_filter_only_shows_matching_posts(self):
        category = Category.objects.create(name="Tecnología")
        self.post.categories.add(category)
        other_post = Post.objects.create(
            title="Otra entrada",
            content="Contenido sin categoría.",
            author=self.user,
        )

        response = self.client.get(
            reverse("blog"), {"categoria": category.slug}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertNotContains(response, other_post.title)
