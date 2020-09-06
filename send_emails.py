import os, sys
import socket
socket.gethostbyname("")
import datetime

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'search_work_service.settings'

import django
django.setup()

from search_work_service.settings import EMAIL_HOST_USER
from search_work_site.models import Error, Url, Vacancy
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model


ADMIN_USER = EMAIL_HOST_USER
today = datetime.date.today()
subject = f'Рассылка вакансий за {today}'
text_content = 'Рассылка вакансий'
from_email = EMAIL_HOST_USER


empty = '<h2>К сожалению на сегодня по Вашим предпочтениям ничего не было найдено</h2>'
User = get_user_model()
queryset = User.objects.filter(send_email = True).values('city', 'language', 'email')
users_dict = {}

for item in queryset:
    users_dict.setdefault((item['city'], item['language']), [])
    users_dict[(item['city'], item['language'])].append(item['email'])
    print('USERS_DICT', users_dict)

if users_dict:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])

    print('PARAMS', params)
    qs = Vacancy.objects.filter(**params, timestamp=today).values()[:10]
    vacancies = {}
    for item in qs:
        print('ITEM', item)
        vacancies.setdefault((item['city_id'], item['language_id']), [])
        vacancies[(item['city_id'], item['language_id'])].append(item)
    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h5 class="card-header"><a href="{row["url"]}">{row["title"]}</a></h5>'
            html += f'<p> {row["description"]}</p><br>'
            html += f'<p> {row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()
            
queryset = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if queryset.exists():
    error = queryset.first()
    data = error.data.get('errors', [])
    print('DATA', data)
    for item in data:
        _html += f'<h4 class="card-header"><a href="{item["url"]}">Error {item["title"]}</a></h4>'
    
    subject = f'Ошибки скрапинга от {today}'
    text_content = 'Ошибки скрапинга'
    data = error.data.get('user_data')
    print('DATA', data)
    if data:
        _html += '<hr>'
        _html += '<h2>Пожелания пользователей</h2>'
        for item in data:
            _html += f'<h4 class="card-header">Город {item["city"]}, Язык программирования {item["language"]} E-mail {item["email"]}</h4>'
    
    subject += f'Пожелания пользователей от {today}'
    text_content += 'Пожелания пользователей '

queryset = Url.objects.all().values('city', 'language')
print('URLS', queryset)
urls_dict = {(item['city'], item['language']): True for item in queryset}
urls_errors = '<hr>'
for keys in users_dict.keys():
    if keys not in urls_dict:
        if keys[0] and keys[1]:
            urls_errors += f'<h4 class="card-header">Для города {keys[0]} и языка программироования {keys[1]} отсутствуют урлы</h4><br>'

if urls_errors:
    subject += ' Отсутствующие урлы'
    _html += urls_errors
if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()

