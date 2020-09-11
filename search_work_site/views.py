from django.contrib import messages
from search_work_site.forms import FindForm, VForm
from search_work_site.models import Vacancy
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
# Create your views here.


def home_view(request):
    form = FindForm()
    return render(request, 'search_work_site/home.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    page_obj = []
    context = {
        'city': city,
        'language': language,
        'form': form
    }
    _filter_dict = dict()
    if city or language:
        if city:
            _filter_dict['city__name'] = city
        if language:
            _filter_dict['language__name'] = language

    all_vacancies = Vacancy.objects.filter(**_filter_dict).select_related('city', 'language')

    paginator = Paginator(all_vacancies, 5)
    
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    context['object_vacancies'] = page_obj
    return render(request, 'search_work_site/list.html', context=context)

def view_detail(request, id=None):
    # object_vacancy = Vacancy.objects.get(pk=id)
    object_vacancy = get_object_or_404(Vacancy, pk=id)
    return render(request, 'search_work_site/detail.html', {'object': object_vacancy})

class VDetail(DetailView):
    queryset = Vacancy.objects.all()
    template_name = 'search_work_site/detail.html'
    # context_object_name = 'object'

class VList(ListView):
    # make template object_list
    # page_obj for pagination
    model = Vacancy
    paginate_by = 10
    template_name = 'search_work_site/list.html'
    form = FindForm()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = self.form
        
        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        qs = []
        if city or language:
            _filter_dict = dict()
            if city:
                _filter_dict['city__name'] = city
            if language:
                _filter_dict['language__name'] = language

            qs = Vacancy.objects.filter(**_filter_dict).select_related('city', 'language')
        return qs

class VCreate(CreateView):
    model = Vacancy
    # fields = '__all__'
    form_class = VForm
    template_name = 'search_work_site/create.html'
    success_url = reverse_lazy('home_page')

class VUpdate(UpdateView):
    model = Vacancy
    # fields = '__all__'
    form_class = VForm
    template_name = 'search_work_site/create.html'
    success_url = reverse_lazy('home_page')

class VDelete(DeleteView):
    model = Vacancy
    # template_name = 'search_work_site/delete.html'
    success_url = reverse_lazy('home_page')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена.')
        return self.post(request, *args, **kwargs)
