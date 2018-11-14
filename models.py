# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Account(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    description = models.CharField(max_length=20, blank=True, null=True)
    account_type = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'account'


class Komik(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    image_url = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'komik'


class List(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(Account, models.DO_NOTHING)
    list_size = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'list'


class Listrank(models.Model):
    list = models.ForeignKey(List, models.DO_NOTHING)
    komik = models.ForeignKey(Komik, models.DO_NOTHING)
    ranking = models.IntegerField()
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'listrank'
        unique_together = (('list', 'ranking'),)


class Review(models.Model):
    user = models.ForeignKey(Account, models.DO_NOTHING)
    komik = models.ForeignKey(Komik, models.DO_NOTHING, primary_key=True)
    rating = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review'
        unique_together = (('komik', 'user'),)


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=20)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tag'


class Tags(models.Model):
    tag = models.ForeignKey(Tag, models.DO_NOTHING, primary_key=True)
    komik = models.ForeignKey(Komik, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tags'
        unique_together = (('tag', 'komik'),)
