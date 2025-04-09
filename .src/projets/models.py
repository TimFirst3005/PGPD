from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, EmailValidator
from django.utils import timezone

class FormeJuridique(models.Model):
    code_forme = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(2)])
    libelle_forme = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Forme juridique"
        verbose_name_plural = "Formes juridiques"
        ordering = ['libelle_forme']

    def __str__(self):
        return self.libelle_forme


class TypeProjet(models.Model):
    code_type = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(2)])
    libelle_type = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Type de projet"
        verbose_name_plural = "Types de projet"
        ordering = ['libelle_type']

    def __str__(self):
        return self.libelle_type


class Promoteur(models.Model):
    PIECE_CHOICES = [
        ('CNI', 'Carte Nationale d\'Identité'),
        ('PASSPORT', 'Passeport'),
        ('PERMIS', 'Permis de conduire'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=150)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    forme_juridique = models.ForeignKey(FormeJuridique, on_delete=models.PROTECT)
    type_piece = models.CharField(max_length=10, choices=PIECE_CHOICES, default='CNI')
    numero_piece = models.CharField(max_length=50)
    piece_identite = models.FileField(upload_to='identites/%Y/%m/%d/')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Promoteur"
        verbose_name_plural = "Promoteurs"
        ordering = ['nom', 'prenom']
        constraints = [
            models.UniqueConstraint(fields=['type_piece', 'numero_piece'], name='unique_piece_identite')
        ]

    def code_promoteur(self):
        return f"{self.nom.upper()[:3]}-{self.date_creation.strftime('%y%m%d')}"

    def __str__(self):
        return f"{self.prenom} {self.nom.upper()}"


class Projet(models.Model):
    STATUT_CHOICES = [
        ('SOUMIS', 'Soumis'),
        ('ETUDE', 'En étude'),
        ('VALIDE', 'Validé'),
        ('REJETE', 'Rejeté'),
    ]

    nom_projet = models.CharField(max_length=100)
    type_projet = models.ForeignKey(TypeProjet, on_delete=models.PROTECT)
    promoteur = models.ForeignKey(Promoteur, on_delete=models.CASCADE)
    description_projet = models.TextField()
    plan_affaire = models.FileField(upload_to='plans_affaire/%Y/%m/%d/')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='SOUMIS')
    date_soumission = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-date_soumission']
        indexes = [
            models.Index(fields=['nom_projet']),
            models.Index(fields=['statut']),
        ]

    def code_projet(self):
        return f"PRJ-{self.id:04d}-{self.date_soumission.strftime('%y')}"

    def __str__(self):
        return f"{self.nom_projet} ({self.get_statut_display()})"