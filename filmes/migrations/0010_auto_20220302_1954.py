# Generated by Django 3.1.5 on 2022-03-02 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filmes', '0009_auto_20220302_1951'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Filmes',
            new_name='Filme',
        ),
        migrations.RenameModel(
            old_name='Ratings',
            new_name='Rating',
        ),
    ]