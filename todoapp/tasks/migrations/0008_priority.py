# Generated by Django 4.2.2 on 2023-07-09 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_alter_comment_task_alter_task_due_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(choices=[('Urgente', 'Urgente'), ('Alta', 'Alta'), ('Media', 'Media'), ('Baja', 'Baja')])),
            ],
        ),
    ]
