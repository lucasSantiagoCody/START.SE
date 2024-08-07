from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import render, redirect
from .models import Company, Document
from django.contrib import messages
from django.urls import reverse

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
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect(reverse('register_company_url'))
        
        

@login_required
def companies_view(request):
    if request.method == 'GET':
        context = {}
        company = Company.objects.filter(user=request.user)
        company_name = request.GET.get('company_name')

        if company_name:
            company = company.filter(name__icontains=company_name)

        context['companies' ] = company

        return render(request, 'companies.html', context)


@login_required
def company_view(request, company_id):
    if request.method == 'GET':
        context = {}
        context['company'] = Company.objects.filter(user=request.user).filter(id=company_id).first
        context['documents'] = Document.objects.filter(company_id=company_id)
        print(context)
        return render(request, 'company.html', context)


@login_required
def add_document_view(request, company_id):
    
    if company := Company.objects.filter(id=company_id).filter(user=request.user)[0]:

        title = request.POST.get('title')
        file = request.FILES.get('file')
        extension = file.name.split('.')

        
        if file or extension[1] == 'pdf':
            try:
                document = Document(
                    company=company,
                    title=title,
                    file=file
                )
                document.save()
                messages.add_message(request, constants.SUCCESS, "Arquivo enviado com sucesso")
            except:
                messages.add_message(request, constants.ERROR, "Erro interno do sistema")
        
        else:
            if extension[1] != 'pdf':
                messages.add_message(request, constants.ERROR, "Envie apenas PDF's")
            elif not file:
                messages.add_message(request, constants.ERROR, "Envie um arquivo")

        return redirect(reverse('company_url', kwargs={'company_id':company_id}))

    else:
        messages.add_message(request, constants.SUCCESS, "Acesso negado")
        return redirect(reverse('login_url'))
    


@login_required
def delete_document_view(request, document_id):
    if request.method == 'GET':
        document = Document.filter(id=document_id)[0]

        if document.company.user != request.user:
            messages.add_message(request, constants.ERROR, "Esse documento não é seu")
            return redirect(reverse('company_url', kwargs={'company_id', document.company.id}))

        document.delete()

        messages.add_message(request, constants.SUCCESS, "Documento excluído com sucesso")
        return redirect(reverse('company_url', kwargs={'company_id', document.company.id}))
