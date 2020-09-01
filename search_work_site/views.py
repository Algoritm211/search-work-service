from search_work_site.forms import FindForm
from search_work_site.models import Vacancy
from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.


def home_view(request):
    form = FindForm()
    return render(request, 'search_work_site/home.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    page_obj = []
    _filter_dict = dict()
    if city or language:
        if city:
            _filter_dict['city__name'] = city
        if language:
            _filter_dict['language__name'] = language

    all_vacancies = Vacancy.objects.filter(**_filter_dict)

    paginator = Paginator(all_vacancies, 5)
    
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, 'search_work_site/list.html', {
        'object_vacancies': page_obj,
        'form': form
        })