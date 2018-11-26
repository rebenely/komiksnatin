# Generated by Django 2.1.3 on 2018-11-25 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('komikrepo', '0006_komik_komik_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='listrank',
            options={'ordering': ('ranking',)},
        ),
        migrations.AddField(
            model_name='list',
            name='list_komiks',
            field=models.ManyToManyField(through='komikrepo.ListRank', to='komikrepo.Komik'),
        ),
    ]