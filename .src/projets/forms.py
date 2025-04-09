from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import FormeJuridique, TypeProjet, Promoteur, Projet
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email

class FormeJuridiqueForm(forms.ModelForm):
    class Meta:
        model = FormeJuridique
        fields = '__all__'
        widgets = {
            'code_forme': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: SARL'}),
            'libelle_forme': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Société à responsabilité limitée'}),
        }

    def clean_code_forme(self):
        code = self.cleaned_data['code_forme'].upper()
        if FormeJuridique.objects.filter(code_forme=code).exists():
            raise ValidationError("Ce code de forme juridique existe déjà.")
        return code


class TypeProjetForm(forms.ModelForm):
    class Meta:
        model = TypeProjet
        fields = '__all__'
        widgets = {
            'code_type': forms.TextInput(attrs={'class': 'form-control'}),
            'libelle_type': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_code_type(self):
        code = self.cleaned_data['code_type'].upper()
        if TypeProjet.objects.filter(code_type=code).exists():
            raise ValidationError("Ce code de type de projet existe déjà.")
        return code


class PromoteurForm(forms.ModelForm):
    confirm_email = forms.EmailField(
        label="Confirmation email",
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Promoteur
        fields = [
            'nom', 'prenom', 'date_naissance', 'lieu_naissance', 
            'email', 'confirm_email', 'forme_juridique', 
            'type_piece', 'numero_piece', 'piece_identite'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'),
            'lieu_naissance': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'forme_juridique': forms.Select(attrs={'class': 'form-control'}),
            'type_piece': forms.Select(attrs={'class': 'form-control'}),
            'numero_piece': forms.TextInput(attrs={'class': 'form-control'}),
            'piece_identite': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'piece_identite': "Pièce d'identité (PDF ou image)",
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')
        
        if email and confirm_email and email != confirm_email:
            self.add_error('confirm_email', "Les emails ne correspondent pas.")
        
        # Validation de l'âge minimum (18 ans)
        date_naissance = cleaned_data.get('date_naissance')
        if date_naissance:
            age = (timezone.now().date() - date_naissance).days // 365
            if age < 18:
                self.add_error('date_naissance', "Le promoteur doit être majeur (18 ans minimum).")
        
        return cleaned_data


class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = ['nom_projet', 'type_projet', 'promoteur', 'description_projet', 'plan_affaire']
        widgets = {
            'nom_projet': forms.TextInput(attrs={'class': 'form-control'}),
            'type_projet': forms.Select(attrs={'class': 'form-control'}),
            'promoteur': forms.Select(attrs={'class': 'form-control'}),
            'description_projet': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Décrivez votre projet en détail...'
            }),
            'plan_affaire': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx'
            }),
        }
        labels = {
            'plan_affaire': "Plan d'affaire (Document)",
        }

    def clean_nom_projet(self):
        nom = self.cleaned_data['nom_projet']
        if len(nom) < 5:
            raise ValidationError("Le nom du projet doit contenir au moins 5 caractères.")
        return nom

    def clean_plan_affaire(self):
        plan = self.cleaned_data['plan_affaire']
        if plan:
            ext = plan.name.split('.')[-1].lower()
            if ext not in ['pdf', 'doc', 'docx', 'xls', 'xlsx']:
                raise ValidationError("Type de fichier non supporté. Formats acceptés: PDF, Word, Excel.")
            if plan.size > 10*1024*1024:  # 10MB
                raise ValidationError("Le fichier est trop volumineux (> 10MB).")
        return plan


class ProjetStatutForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = ['statut']
        widgets = {
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }


class PromoteurSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom, prénom ou email...'
        })
    )
    forme_juridique = forms.ModelChoiceField(
        queryset=FormeJuridique.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ProjetSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom du projet ou promoteur...'
        })
    )
    type_projet = forms.ModelChoiceField(
        queryset=TypeProjet.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    statut = forms.ChoiceField(
        choices=[('', 'Tous les statuts')] + Projet.STATUT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )