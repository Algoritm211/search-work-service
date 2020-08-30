import codecs
import os, sys


project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'search_work_service.settings'


import django
django.setup()

from django.db import DatabaseError
from search_work_site.parsers import *
from search_work_site.models import City, Vacancy, Language, Error


parsers = (
    (work_ua, 'https://www.work.ua/ru/jobs-kyiv-python'),
    (dou_ua, 'https://jobs.dou.ua/vacancies/?city=Киев&search=Python'),
    (djinni_ua, 'https://djinni.co/jobs/?primary_keyword=Python&location=Киев'),
    (rabota_ua, 'https://rabota.ua/zapros/python/киев'),
)

city = City.objects.filter(name='Киев').first()
language = Language.objects.filter(name='Python').first()
jobs, errors = [], []

for func, url in parsers:
    jbs, errs = func(url)
    jobs += jbs
    errors += errs

for job in jobs:
    vacancy = Vacancy(**job, city=city, language=language)
    try:
        vacancy.save()
    except DatabaseError:
        err = Error(data=errors).save

    # with codecs.open('work.json', 'w', 'utf-8') as file:
    #     file.write(str(jobs))