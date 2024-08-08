from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.db import models
from datetime import date

class Company(models.Model):
    existence_time_choices = (
        ('-6', 'Menos de 6 meses'),
        ('+6', 'Mais de 6 meses'),
        ('+1', 'Mais de 1 ano'),
        ('+5', 'Mais de 5 anos')
        
    )
    internship_choices = (
        ('I', 'Tenho apenas uma idea'),
        ('MVP', 'Possuo um MVP'),
        ('MVPP', 'Possuo um MVP com clientes pagantes'),
        ('E', 'Empresa pronta para escalar'),
    )
    sector_choices = (
        ('ED', 'Ed-tech'),
        ('FT', 'Fintech'),
        ('AT', 'Agrotech'),
        
    )
    class Meta:
        verbose_name_plural = 'companies'
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=30)
    site = models.URLField()
    existence_time = models.CharField(max_length=2, choices=existence_time_choices, default='-6')
    description = models.TextField() 
    # data final captação
    captation_final_date = models.DateField()
    percentage_equity = models.IntegerField() # Percentual esperado
    internship = models.CharField(max_length=4, choices=internship_choices, default='I')
    sector = models.CharField(max_length=3, choices=sector_choices)
    target_audience = models.CharField(max_length=3)
    value = models.DecimalField(max_digits=9, decimal_places=2) # Valor total a ser vendido
    pitch = models.FileField(upload_to='pitches')
    logo = models.FileField(upload_to='logo')


    @property
    def status(self):
        if date.today() > self.captation_final_date:
            return mark_safe('<span class="badge bg-success">Captação finalizada</span>')
        return mark_safe('<span class="badge bg-primary">Em captação</span>')

    @property
    def valuation(self):
        return (100 * self.value) / self.percentage_equity

    def __str__(self):
        return f'{self.user.username} | {self.name}'
    
class Document(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    file = models.FileField(upload_to="documents")

    def __str__(self):
        return self.title



class Metric(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    value = models.FloatField()

    def __str__(self):
        return self.title