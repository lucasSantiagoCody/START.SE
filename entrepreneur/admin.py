from django.contrib import admin
from .models import Company, Document, Metric

admin.site.register(Company)
admin.site.register(Document)
admin.site.register(Metric)
