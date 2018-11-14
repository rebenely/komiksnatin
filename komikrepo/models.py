# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(primary_key=True, max_length=20)
    description = models.CharField(max_length=500, blank=True, null=True)
    account_type = models.CharField(max_length=20)

    class Meta:

        db_table = 'account'


    @receiver(post_save, sender=User)
    def update_user_account(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user=instance, username=instance.username)
        instance.account.save()




class List(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(Account, models.DO_NOTHING)
    list_size = models.IntegerField()

    class Meta:

        db_table = 'list'







class Tag(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'tag'
    def __str__(self):
        return self.name

class Komik(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    komik_tags = models.ManyToManyField(Tag, through='Tags')

    def __str__(self):
        return self.title

    class Meta:

        db_table = 'komik'

class Tags(models.Model):
    tag = models.ForeignKey(Tag, models.DO_NOTHING)
    komik = models.ForeignKey(Komik, models.DO_NOTHING)


    def __str__(self):
        return self.komik.title + ':' + self.tag.name

    class Meta:

        db_table = 'tags'
        unique_together = (('tag', 'komik'),)

class ListRank(models.Model):
    list = models.ForeignKey(List, models.DO_NOTHING)
    komik = models.ForeignKey(Komik, models.DO_NOTHING)
    ranking = models.IntegerField()
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:

        db_table = 'listrank'
        unique_together = (('list', 'ranking'),)

class Review(models.Model):
    user = models.ForeignKey(Account, models.DO_NOTHING)
    komik = models.ForeignKey(Komik, models.DO_NOTHING)
    rating = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)

    class Meta:

        db_table = 'review'
        unique_together = (('komik', 'user'),)
