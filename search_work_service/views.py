from django.http import HttpResponse
from django.shortcuts import redirect


def redirect_to_home_page(request):
    return redirect('home_page', permanent=True)
