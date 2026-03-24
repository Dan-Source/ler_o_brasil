from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0008_authorpage_author_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="authorpage",
            old_name="author_image",
            new_name="avatar",
        ),
    ]
