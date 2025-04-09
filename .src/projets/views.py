from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import FormeJuridique, TypeProjet, Promoteur, Projet
from .forms import (
    FormeJuridiqueForm, TypeProjetForm, PromoteurForm, 
    ProjetForm, ProjetStatutForm, PromoteurSearchForm, ProjetSearchForm
)

## Vues pour FormeJuridique ##
class FormeJuridiqueListView(LoginRequiredMixin, ListView):
    model = FormeJuridique
    template_name = 'projets/forme_juridique/list.html'
    context_object_name = 'formes_juridiques'
    paginate_by = 10

    def get_queryset(self):
        return FormeJuridique.objects.all().order_by('libelle_forme')


class FormeJuridiqueCreateView(LoginRequiredMixin, CreateView):
    model = FormeJuridique
    form_class = FormeJuridiqueForm
    template_name = 'projets/forme_juridique/create.html'
    success_url = reverse_lazy('projets:forme_juridique_list')

    def form_valid(self, form):
        messages.success(self.request, "La forme juridique a été créée avec succès.")
        return super().form_valid(form)


class FormeJuridiqueDetailView(LoginRequiredMixin, DetailView):
    model = FormeJuridique
    template_name = 'projets/forme_juridique/detail.html'
    context_object_name = 'forme_juridique'


## Vues pour TypeProjet ##
class TypeProjetListView(LoginRequiredMixin, ListView):
    model = TypeProjet
    template_name = 'projets/type_projet/list.html'
    context_object_name = 'types_projet'
    paginate_by = 10

    def get_queryset(self):
        return TypeProjet.objects.all().order_by('libelle_type')


class TypeProjetCreateView(LoginRequiredMixin, CreateView):
    model = TypeProjet
    form_class = TypeProjetForm
    template_name = 'projets/type_projet/create.html'
    success_url = reverse_lazy('projets:type_projet_list')

    def form_valid(self, form):
        messages.success(self.request, "Le type de projet a été créé avec succès.")
        return super().form_valid(form)


class TypeProjetDetailView(LoginRequiredMixin, DetailView):
    model = TypeProjet
    template_name = 'projets/type_projet/detail.html'
    context_object_name = 'type_projet'


## Vues pour Promoteur ##
class PromoteurListView(LoginRequiredMixin, ListView):
    model = Promoteur
    template_name = 'projets/promoteur/list.html'
    context_object_name = 'promoteurs'
    paginate_by = 10

    def get_queryset(self):
        return Promoteur.objects.all().order_by('nom', 'prenom')


class PromoteurCreateView(LoginRequiredMixin, CreateView):
    model = Promoteur
    form_class = PromoteurForm
    template_name = 'projets/promoteur/create.html'
    success_url = reverse_lazy('projets:promoteur_list')

    def form_valid(self, form):
        messages.success(self.request, "Le promoteur a été créé avec succès.")
        return super().form_valid(form)


class PromoteurDetailView(LoginRequiredMixin, DetailView):
    model = Promoteur
    template_name = 'projets/promoteur/detail.html'
    context_object_name = 'promoteur'


def promoteur_search(request):
    form = PromoteurSearchForm(request.GET or None)
    promoteurs = Promoteur.objects.all()

    if form.is_valid():
        search = form.cleaned_data.get('search')
        forme_juridique = form.cleaned_data.get('forme_juridique')

        if search:
            promoteurs = promoteurs.filter(
                Q(nom__icontains=search) | 
                Q(prenom__icontains=search) |
                Q(email__icontains=search)
            )
        
        if forme_juridique:
            promoteurs = promoteurs.filter(forme_juridique=forme_juridique)

    context = {
        'form': form,
        'promoteurs': promoteurs,
        'search_performed': any(field in request.GET for field in ['search', 'forme_juridique'])
    }
    return render(request, 'projets/promoteur/search.html', context)


## Vues pour Projet ##
class ProjetListView(LoginRequiredMixin, ListView):
    model = Projet
    template_name = 'projets/projet/list.html'
    context_object_name = 'projets'
    paginate_by = 10

    def get_queryset(self):
        return Projet.objects.all().order_by('-date_soumission')


class ProjetCreateView(LoginRequiredMixin, CreateView):
    model = Projet
    form_class = ProjetForm
    template_name = 'projets/projet/create.html'
    success_url = reverse_lazy('projets:projet_list')

    def form_valid(self, form):
        messages.success(self.request, "Le projet a été créé avec succès.")
        return super().form_valid(form)


class ProjetDetailView(LoginRequiredMixin, DetailView):
    model = Projet
    template_name = 'projets/projet/detail.html'
    context_object_name = 'projet'


def projet_search(request):
    form = ProjetSearchForm(request.GET or None)
    projets = Projet.objects.all()

    if form.is_valid():
        search = form.cleaned_data.get('search')
        type_projet = form.cleaned_data.get('type_projet')
        statut = form.cleaned_data.get('statut')

        if search:
            projets = projets.filter(
                Q(nom_projet__icontains=search) | 
                Q(promoteur__nom__icontains=search) |
                Q(promoteur__prenom__icontains=search)
            )
        
        if type_projet:
            projets = projets.filter(type_projet=type_projet)
        
        if statut:
            projets = projets.filter(statut=statut)

    context = {
        'form': form,
        'projets': projets,
        'search_performed': any(field in request.GET for field in ['search', 'type_projet', 'statut'])
    }
    return render(request, 'projets/projet/search.html', context)


class ProjetUpdateStatutView(LoginRequiredMixin, UpdateView):
    model = Projet
    form_class = ProjetStatutForm
    template_name = 'projets/projet/update_statut.html'
    context_object_name = 'projet'

    def get_success_url(self):
        messages.success(self.request, "Le statut du projet a été mis à jour.")
        return reverse_lazy('projets:projet_detail', kwargs={'pk': self.object.pk})