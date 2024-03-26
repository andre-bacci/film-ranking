from django.contrib import admin

from .models import Compilation, List, Ranking

admin.site.register(List)
admin.site.register(Ranking)
admin.site.register(Compilation)
