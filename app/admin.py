from django.contrib import admin
from .models import Patient, Psychologist, Entry

# Register your models here.
admin.site.register(Patient)
admin.site.register(Psychologist)
admin.site.register(Entry)

