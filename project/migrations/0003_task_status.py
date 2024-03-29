# Generated by Django 5.0.2 on 2024-02-28 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0002_note_category_project_status_task_difficulty_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[
                    ("To Do", "To Do"),
                    ("In Progress", "In Progress"),
                    ("Done", "Done"),
                ],
                default="To Do",
                max_length=20,
            ),
        ),
    ]
