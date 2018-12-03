# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Account(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    description = models.CharField(max_length=200, blank=True, null=True)
    accounttype = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'account'

    @receiver(post_save, sender=User)
    def update_user_account(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user=instance, username=instance.username)
        instance.account.save()
    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tag'
    def __str__(self):
        return self.name


class Komik(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.CharField(max_length=500)
    komik_tags = models.ManyToManyField(Tag, through='Tags')

    class Meta:
        managed = False
        db_table = 'komik'
    def __str__(self):
        return self.title

class Tags(models.Model):
    komik = models.ForeignKey(Komik, models.CASCADE)
    tag = models.ForeignKey(Tag, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'tags'

class Review(models.Model):
    user = models.ForeignKey(Account, models.CASCADE)
    komik = models.ForeignKey(Komik, models.CASCADE)
    rating = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review'
        unique_together = (('komik', 'user'),)

class List(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True, null=True)
    list_size = models.IntegerField()
    user = models.ForeignKey(Account, models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    list_komiks = models.ManyToManyField(Komik, through='ListRank')


    class Meta:
        managed = False
        db_table = 'list'


class ListRank(models.Model):
    ranking = models.IntegerField()
    description = models.CharField(max_length=1000, blank=True, null=True)
    komik = models.ForeignKey(Komik, models.CASCADE)
    list = models.ForeignKey(List, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'listrank'
        unique_together = (('list', 'ranking'), ('list', 'komik'),)
