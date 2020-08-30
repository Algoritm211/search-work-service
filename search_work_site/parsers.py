import requests
import codecs
from bs4 import BeautifulSoup

__all__ = ('work_ua', 'rabota_ua', 'dou_ua', 'djinni_ua')

headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Accept-Language': 'ru'
        }

def work_ua(url):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        main_div = soup.find('div', id='pjax-job-list')
        if main_div:
            div_list = main_div.find_all('div', attrs={'class': 'job-link'})
            for div in div_list:
                title = div.find('h2').text
                href = domain + div.a['href']
                content = div.p.text
                company = 'No company'
                logo = div.find('img')
                if logo:
                    company = logo['alt']
                jobs.append({
                    'title': title,
                    'url': href,
                    'description': content,
                    'company': company
                    })
        else:
            errors.append({'url': url, 'title': 'Div does not response'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def rabota_ua(url):
    jobs = []
    errors = []
    domain = 'https://rabota.ua'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        new_jobs = soup.find('div', attrs={'class': 'f-vacancylist-newnotfound'})
        if not new_jobs:
            table = soup.find('table', id='ctl00_content_vacancyList_gridList')
            if table:
                tr_list = table.find_all('tr', attrs={'id': True})
                for tr in tr_list:
                    div = tr.find('div', attrs={'class': 'card-body'})
                    if div:
                        title = div.find('p', attrs={'class': 'card-title'}).text
                        href = domain + div.find('p', attrs={'class': 'card-title'}).a['href']
                        content = div.p.text
                        company = 'No company'
                        p = div.find('p', attrs={'class': 'company-name'})
                        if p:
                            company = p.a.text
                        jobs.append({
                            'title': title,
                            'url': href,
                            'description': content,
                            'company': company
                            })
            else:
                errors.append({'url': url, 'title': 'Table does not response'})
        else:
            errors.append({'url': url, 'title': 'Page is empty'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})
    
    return jobs, errors


def dou_ua(url):
    jobs = []
    errors = []
    # domain = 'https://www.work.ua'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        main_div = soup.find('div', id='vacancyListId')
        if main_div:
            li_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})
            for li in li_list:
                title = li.find('div', attrs={'class': 'title'}).text.strip()
                href = li.find('div', attrs={'class': 'title'}).a['href']
                content = li.find('div', attrs={'class': 'sh-info'}).text.strip()
                company = 'No company'
                a = li.find('div', attrs={'class': 'title'}).find('a', attrs={'class': 'company'})
                if a:
                    company = a.text
                jobs.append({
                    'title': title,
                    'url': href,
                    'description': content,
                    'company': company
                    })
        else:
            errors.append({'url': url, 'title': 'Div does not response'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def djinni_ua(url):
    jobs = []
    errors = []
    domain = 'https://djinni.co'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
        if main_ul:
            li_list = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
            for li in li_list:
                title = li.find('div', attrs={'class': 'list-jobs__title'}).text
                href = domain + li.find('div', attrs={'class': 'list-jobs__title'}).a['href']
                content = li.find('div', attrs={'class': 'list-jobs__description'}).text
                company = 'No company'
                div = li.find('div', attrs={'class': 'list-jobs__title'}).find('div', attrs={'class': 'list-jobs__details__info'})
                if div:
                    company = div.a.text
                jobs.append({
                    'title': title,
                    'url': href,
                    'description': content,
                    'company': company
                    })
        else:
            errors.append({'url': url, 'title': 'Div does not response'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


if __name__ == '__main__':
    url = 'https://jobs.dou.ua/vacancies/?city=Киев&search=Python'
    jobs, errors = dou_ua(url)
    with codecs.open('work.json', 'w', 'utf-8') as file:
        file.write(str(jobs))