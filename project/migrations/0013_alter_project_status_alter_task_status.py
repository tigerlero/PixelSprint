# Generated by Django 5.0.2 on 2024-03-02 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0012_status_alter_task_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="status",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="projects",
                to="project.status",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="project.status",
            ),
        ),
    ]
