# Generated by Django 4.2.1 on 2023-06-07 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_comments_project_alter_comments_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='projects.projects'),
        ),
    ]
