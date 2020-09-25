from asyncio import tasks
import codecs
import os, sys
# from send_emails import error
import asyncio
import datetime


project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'search_work_service.settings'


import django
django.setup()

from django.contrib.auth import get_user_model
from django.db import DatabaseError
from search_work_site.parsers import *
from search_work_site.models import City, Vacancy, Language, Error, Url

User = get_user_model()

parsers = (
    (work_ua, 'work_ua'),
    (dou_ua, 'dou_ua'),
    (djinni_ua, 'djinni_ua'),
    (rabota_ua, 'rabota_ua'),
)

jobs, errors = [], []

def get_settings():
    queryset = User.objects.filter(send_email=True).values()
    # print(queryset)
    settings_list = set((qs['city_id'], qs['language_id']) for qs in queryset)
    # print(settings_list)
    return settings_list

def get_urls(_settings):
    # print(_settings)
    queryset = Url.objects.all().values()
    url_dict = {(qs['city_id'], qs['language_id']): qs['url_data'] for qs in queryset}
    urls = []
    print('URLDICT', url_dict)

    for pair in _settings:
        temp = {}
        if pair in url_dict:
            temp['city'] = pair[0]
            temp['language'] = pair[1]
            temp['url_data'] = url_dict[pair]
        urls.append(temp)

    return urls

async def main(value):
    func, url, city, language = value
    # print('VALUE ', value)
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)


settings = get_settings()
url_list = get_urls(settings)


loop = asyncio.get_event_loop()
temp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
            for data in url_list
            for func, key in parsers]
tasks = asyncio.wait([loop.create_task(main(f)) for f in temp_tasks])            
# for data in url_list:
#     # print('DATA', data)
#     for func, key in parsers:
#         url = data['url_data'][key]
#         # print('URL', url)
#         jbs, errs = func(url, city=data['city'], language=data['language'])
#         jobs += jbs
#         errors += errs

loop.run_until_complete(tasks)
loop.close()

for job in jobs:
    vacancy = Vacancy(**job)
    try:
        vacancy.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(timestamp=datetime.date.today())
    if qs.exists():
        err = qs.first()
        data = err.data
        # err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'errors: {errors}').save()


    # with codecs.open('work.json', 'w', 'utf-8') as file:
    #     file.write(str(jobs))