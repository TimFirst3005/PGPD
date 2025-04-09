# projets/urls.py

from django.urls import path
from . import views

app_name = 'projets'

urlpatterns = [
    # URLs pour FormeJuridique
    path('formes-juridiques/', 
         views.FormeJuridiqueListView.as_view(), 
         name='forme_juridique_list'),
    path('formes-juridiques/nouvelle/', 
         views.FormeJuridiqueCreateView.as_view(), 
         name='forme_juridique_create'),
    path('formes-juridiques/<int:pk>/', 
         views.FormeJuridiqueDetailView.as_view(), 
         name='forme_juridique_detail'),
    
    # URLs pour TypeProjet
    path('types-projet/', 
         views.TypeProjetListView.as_view(), 
         name='type_projet_list'),
    path('types-projet/nouveau/', 
         views.TypeProjetCreateView.as_view(), 
         name='type_projet_create'),
    path('types-projet/<int:pk>/', 
         views.TypeProjetDetailView.as_view(), 
         name='type_projet_detail'),
    
    # URLs pour Promoteur
    path('promoteurs/', 
         views.PromoteurListView.as_view(), 
         name='promoteur_list'),
    path('promoteurs/nouveau/', 
         views.PromoteurCreateView.as_view(), 
         name='promoteur_create'),
    path('promoteurs/<int:pk>/', 
         views.PromoteurDetailView.as_view(), 
         name='promoteur_detail'),
    path('promoteurs/recherche/', 
         views.promoteur_search, 
         name='promoteur_search'),
    
    # URLs pour Projet
    path('', 
         views.ProjetListView.as_view(), 
         name='projet_list'),
    path('projets/nouveau/', 
         views.ProjetCreateView.as_view(), 
         name='projet_create'),
    path('projets/<int:pk>/', 
         views.ProjetDetailView.as_view(), 
         name='projet_detail'),
    path('projets/recherche/', 
         views.projet_search, 
         name='projet_search'),
    path('projets/<int:pk>/modifier-statut/', 
         views.ProjetUpdateStatutView.as_view(), 
         name='projet_update_statut'),
]