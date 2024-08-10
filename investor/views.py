from django.shortcuts import render, redirect, get_object_or_404
from entrepreneur.models import Company, Document
from django.contrib.messages import constants
from .models import InvestmentProposal
from django.contrib import messages
from django.urls import reverse



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
        context['company' ] = company
        context['documents' ] = documents

        return render(request, 'company_details.html', context)

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
        return redirect(f'/investidores/assinar_contrato/{investment_proposal.id}')
    
    return redirect(reverse('company_details_url', kwargs={'company_id': company_id}))
    

    