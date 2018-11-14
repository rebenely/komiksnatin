# Generated by Django 2.1.3 on 2018-11-13 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('komikrepo', '0002_auto_20181112_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='komik',
            name='author',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='komik',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='list',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]