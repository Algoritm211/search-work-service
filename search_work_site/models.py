import datetime
from django.db import models
import jsonfield

# Create your models here.


class City(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название населенного пункта',
        unique=True)

    slug = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Ссылка')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            now = datetime.datetime.now()
            timestamp = str(int(datetime.datetime.timestamp(now)))
            self.slug = timestamp
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Language(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Язык программирования',
        unique=True)

    slug = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Ссылка')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            now = datetime.datetime.now()
            timestamp = str(int(datetime.datetime.timestamp(now)))
            self.slug = timestamp
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'


class Vacancy(models.Model):
    url = models.URLField(verbose_name='Ссылка на вакансию', unique=True)
    title = models.CharField(max_length=200, verbose_name='Название вакансии')
    company = models.CharField(max_length=200, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание')
    city = models.ForeignKey(
        'City', on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey(
        'Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()
