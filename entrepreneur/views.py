from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Company

@login_required
def register_company_view(request):
    if request.method ==  'GET':
        context = {}
        context['existence_time_choices'] = Company.existence_time_choices
        context['sector_choices'] = Company.sector_choices
        return render(request, 'register_company.html', context)
    elif request.method == 'POST':
        name = request.POST.get('name')
        cnpj = request.POST.get('cnpj')
        site = request.POST.get('site')
        existence_time = request.POST.get('existence_time')
        description = request.POST.get('description')
        captation_final_date = request.POST.get('captation_final_date')
        percentage_equity = request.POST.get('percentage_equity')
        internship = request.POST.get('internship')
        sector = request.POST.get('sector')
        target_audience = request.POST.get('target_audience')
        value = request.POST.get('value')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')

        try:
            empresa = Company(
                user=request.user,
                name=name,
                cnpj=cnpj,
                site=site,
                existence_time=existence_time,
                description=description,
                captation_final_date=captation_final_date,
                percentage_equity=percentage_equity,
                internship=internship,
                sector=sector,
                target_audience=target_audience,
                value=value,
                pitch=pitch,
                logo=logo
            )
            empresa.save()

            messages.add_message(request, constants.SUCCESS, 'Empresa registrada com sucesso')
            return redirect(reverse('register_company_url'))
        except Exception as e:
            print(e)
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect(reverse('register_company_url'))
        
        