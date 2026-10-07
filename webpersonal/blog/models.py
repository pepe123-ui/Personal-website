from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to="blog/images/", blank=True, null=True)
    media_file = models.FileField(
        upload_to="blog/media/",
        blank=True,
        null=True,
        help_text="Imagen, audio o video opcional.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    class Meta:
        db_table = "portfolio_post"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "entrada"
            slug = base
            n = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_comments",
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "portfolio_comment"
        ordering = ["created_at"]

    def __str__(self):
        return f"Comentario de {self.author} en {self.post}"
