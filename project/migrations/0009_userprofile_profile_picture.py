# Generated by Django 5.0.2 on 2024-03-01 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0008_remove_userprofile_profile_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="profile_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="profile_pictures/"
            ),
        ),
    ]
