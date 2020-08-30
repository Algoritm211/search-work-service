from search_work_site.forms import FindForm
from search_work_site.models import Vacancy
from django.shortcuts import render

# Create your views here.


def home_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    all_vacancies = []
    _filter_dict = dict()
    if city or language:
        if city:
            _filter_dict['city__name'] = city
        if language:
            _filter_dict['language__name'] = language

    all_vacancies = Vacancy.objects.filter(**_filter_dict)
    return render(request, 'search_work_site/home.html', {
        'object_vacancies': all_vacancies,
        'form': form
        })
