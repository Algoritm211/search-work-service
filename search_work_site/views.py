from search_work_site.models import Vacancy
from django.shortcuts import render

# Create your views here.


def home_view(request):
    all_vacancies = Vacancy.objects.all()
    return render(request, 'search_work_site/home.html', {'object_vacancies': all_vacancies})
