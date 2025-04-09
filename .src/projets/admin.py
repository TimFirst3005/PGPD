from django.contrib import admin
from .models import Projet, Promoteur, TypeProjet, FormeJuridique

# Register your models here.

admin.site.register(Projet)
admin.site.register(Promoteur)
admin.site.register(TypeProjet)
admin.site.register(FormeJuridique)