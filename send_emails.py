from search_work_service.settings import EMAIL_HOST_USER
from run_scraping import vacancy
from search_work_site.models import Vacancy
import django
import os, sys
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth import get_user_model

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'search_work_service.settings'

django.setup()

subject = 'Рассылка вакансий'
text_content = 'Рассылка вакансий'
from_email = EMAIL_HOST_USER


empty = '<h2>К сожалению на сегодня по Вашим предпочтениям ничего не было найдено</h2>'
User = get_user_model()
queryset = User.objects.filter(send_email = True).values('city', 'language', 'email')
print('QUERYSET', queryset)
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
    qs = Vacancy.objects.filter(**params).values()[:10]
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
            # try:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()
            # except:
            #     print(email)
            

