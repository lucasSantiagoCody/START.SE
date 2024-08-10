from django.shortcuts import render, get_object_or_404
from entrepreneur.models import Company, Document



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
