# Generated by Django 5.0.2 on 2024-03-10 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0022_remove_task_effort_remove_task_is_archived_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="tags_input",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]