# Generated by Django 3.1 on 2020-08-30 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название населенного пункта')),
                ('slug', models.CharField(blank=True, max_length=200, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Язык программирования')),
                ('slug', models.CharField(blank=True, max_length=200, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Язык программирования',
                'verbose_name_plural': 'Языки программирования',
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True, verbose_name='Ссылка на вакансию')),
                ('title', models.CharField(max_length=200, verbose_name='Название вакансии')),
                ('company', models.CharField(max_length=200, verbose_name='Компания')),
                ('description', models.TextField(verbose_name='Описание')),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search_work_site.city', verbose_name='Город')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search_work_site.language', verbose_name='Язык программирования')),
            ],
            options={
                'verbose_name': 'Вакансия',
                'verbose_name_plural': 'Вакансии',
            },
        ),
    ]
