from django.contrib import admin

from .models import Credit, Film, Person

admin.site.register(Film)
admin.site.register(Person)
admin.site.register(Credit)
