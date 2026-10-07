from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name="Comment"),
                migrations.DeleteModel(name="Post"),
            ],
            database_operations=[],
        ),
    ]
