from django.contrib import admin
from .models import Country, Province, City, ImpParam

# Register your models here.

admin.site.register(Country)
admin.site.register(ImpParam)
admin.site.register(Province)
admin.site.register(City)
