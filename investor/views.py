from django.shortcuts import render, redirect, get_object_or_404
from entrepreneur.models import Company, Document
from django.contrib.messages import constants
from .models import InvestmentProposal
from django.contrib import messages
from django.urls import reverse
from django.http import Http404

def suggestion_view(request):
    if request.method == 'GET':
        context = {}
        context['sector_choices'] = Company.sector_choices

        investor_type = request.GET.get('type')
        sector = request.GET.get('sector')
        value = request.GET.get('value')


        if investor_type and sector and value:

            existence_time_on_investor_type = {
                'C': Company.objects.filter(existence_time='+5').filter(internship='E'),
                'D': Company.objects.filter(existence_time__in=['-6', '+1', '+6']).exclude(internship='E')
                }
            
            companies = existence_time_on_investor_type[investor_type]
            companies.filter(sector__in=sector)
            

            chosen_companies = []
            for company in companies:
                percentage = (float(value) * 100) / float(company.valuation)
                if percentage >= 1:
                    chosen_companies.append(company)
                    
            context['chosen_companies'] = chosen_companies
        
        return render(request, 'suggestion.html', context)

        
def company_details_view(request, company_id):
    if request.method == 'GET':
        context = {}
        company = get_object_or_404(Company, id=company_id)
        documents = Document.objects.filter(company=company)
        investments_proposal = InvestmentProposal.objects.filter(company_id=company_id)

        percentage_sold = 0
        for investments_proposal in investments_proposal:
            percentage_sold = percentage_sold + investments_proposal.percentage

        limiar = (80 * company.percentage_equity) / 100

        realized = False
        if percentage_sold >= limiar:
            realized = True

        available_percentage = company.percentage_equity - percentage_sold

        context['company' ] = company
        context['documents' ] = documents
        context['percentage_sold' ] = percentage_sold
        context['realized' ] = realized
        context['available_percentage' ] = available_percentage

        return render(request, 'investor_company_details.html', context)

def make_proposal_view(request, company_id):
    value = request.POST.get('value')
    percentage = request.POST.get('percentage')
    company = get_object_or_404(Company, id=company_id)

    valuation = (100 * int(value)) / int(percentage)


    accepted_proposals = InvestmentProposal.objects.filter(company=company).filter(status='PA')
    total = 0
    for accepted_proposal in accepted_proposals:
        total = total + accepted_proposal.percentage

    if total + int(percentage)  > company.percentage_equity:
        messages.add_message(request, constants.WARNING, 'O percentual solicitado ultrapassa o percentual máximo.')
    elif not value or not percentage:
        messages.add_message(request, constants.WARNING, 'Prencha os campos valor para investor e percentual esperado')
    elif valuation < (int(company.valuation) / 2):
        messages.add_message(request, constants.WARNING, f'Seu valuation proposto foi R${valuation} e deve ser no mínimo R${company.valuation/2}')
    else:

        investment_proposal = InvestmentProposal(
            value=value,
            percentage=percentage,
            company=company,
            investor=request.user,
        )

        investment_proposal.save()

        messages.add_message(request, constants.SUCCESS, f'Proposta enviada com sucesso')
        return redirect(reverse('sign_contract_url', kwargs={'investment_proposal_id': investment_proposal.id}))
    
    return redirect(reverse('company_details_url', kwargs={'company_id': company_id}))
    

    


def sign_contract_view(request, investment_proposal_id):
    investment_proposal = InvestmentProposal.objects.get(id=investment_proposal_id)

    if investment_proposal.status != "AS":
        raise Http404()
    
    if request.method == "GET":
        context = {}
        context['investment_proposal_id'] = investment_proposal_id
        return render(request, 'sign_contract.html', context)
    
    elif request.method == "POST":
        selfie = request.FILES.get('selfie')
        rg = request.FILES.get('rg')
        

        investment_proposal.selfie = selfie
        investment_proposal.rg = rg
        investment_proposal.status = 'PE'
        investment_proposal.save()

        messages.add_message(request, constants.SUCCESS, f'Contrato assinado com sucesso, sua proposta foi enviada a empresa.')
        return redirect(reverse('company_details_url', kwargs={'company_id': investment_proposal.company.id}))
