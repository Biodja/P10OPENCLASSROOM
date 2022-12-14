# Generated by Django 4.1 on 2022-09-05 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("API", "0002_remove_project_project_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="issue",
            name="issue_comment",
            field=models.ManyToManyField(
                related_name="issue_comment",
                through="API.Comment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="project_members",
            field=models.ManyToManyField(
                related_name="project_contributor",
                through="API.Contributor",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="issue",
            name="project_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="API.project"
            ),
        ),
    ]
