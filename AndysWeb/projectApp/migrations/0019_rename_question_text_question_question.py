# Generated by Django 4.0.1 on 2022-06-29 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectApp', '0018_question_choice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question_text',
            new_name='question',
        ),
    ]