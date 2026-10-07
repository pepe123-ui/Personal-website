import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name="Post",
                    fields=[
                        (
                            "id",
                            models.BigAutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        ),
                        ("title", models.CharField(max_length=200)),
                        (
                            "slug",
                            models.SlugField(
                                blank=True, max_length=220, unique=True
                            ),
                        ),
                        ("content", models.TextField()),
                        (
                            "image",
                            models.ImageField(
                                blank=True,
                                null=True,
                                upload_to="blog/images/",
                            ),
                        ),
                        (
                            "media_file",
                            models.FileField(
                                blank=True,
                                help_text="Imagen, audio o video opcional.",
                                null=True,
                                upload_to="blog/media/",
                            ),
                        ),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                        ("updated_at", models.DateTimeField(auto_now=True)),
                        (
                            "author",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="posts",
                                to=settings.AUTH_USER_MODEL,
                            ),
                        ),
                    ],
                    options={
                        "db_table": "portfolio_post",
                        "ordering": ["-created_at"],
                    },
                ),
                migrations.CreateModel(
                    name="Comment",
                    fields=[
                        (
                            "id",
                            models.BigAutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        ),
                        ("body", models.TextField()),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                        (
                            "author",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="blog_comments",
                                to=settings.AUTH_USER_MODEL,
                            ),
                        ),
                        (
                            "post",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="comments",
                                to="blog.post",
                            ),
                        ),
                    ],
                    options={
                        "db_table": "portfolio_comment",
                        "ordering": ["created_at"],
                    },
                ),
            ],
            database_operations=[],
        ),
    ]
