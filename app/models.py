from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UsuarioManager



# Create your models here.

class CNPJ(models.Model):
    razao_social = models.CharField(max_length=50, blank=False, null=False, verbose_name='Razão Social')
    nome_fantasia = models.CharField(max_length=50, blank=False, null=False, verbose_name='Nome Fantasia')
    cnpj = models.CharField(max_length=14, blank=False, null=False, verbose_name='CNPJ')
    criado = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nome_fantasia

class Usuario(AbstractUser, PermissionsMixin):
    CARGO = (
        ('ADM', 'Administrativo'),
        ('LD', 'Lider'),
        ('USER', 'Operacional')
    )

    username = models.CharField(max_length=10, unique=False, blank=True, null=True, default="")
    codigo = models.CharField(_("Codigo"), unique=True, max_length=6)
    nome = models.CharField(_('Nome'), max_length=20)
    setor = models.CharField(_('Setor'), max_length=15, choices=CARGO, default='USER')
    empresa = models.ForeignKey(CNPJ, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='users')


    USERNAME_FIELD = 'codigo'
    REQUIRED_FIELDS = ['nome']

    objects = UsuarioManager()

    def __str__(self)-> str:
        return self.nome
    
    def data(self)->dict:
        return {
            'nome': self.nome,
            'setor': self.setor
        }


class Ponto(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name='pontos')
    data = models.DateField()
    motivo = models.CharField(max_length=150)
    empresa = models.ForeignKey(CNPJ, on_delete=models.DO_NOTHING, related_name='pontos')
    

class Marca(models.Model):
    marca = models.CharField(max_length=30, verbose_name='Marca')
    criado = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name='marcas')
    empresa = models.ForeignKey(CNPJ, on_delete=models.DO_NOTHING, related_name='marcas')

    def __str__(self)-> str:
        return self.marca


class Produto(models.Model):
    nome = models.CharField(max_length=30, verbose_name='Produto')
    marca = models.ForeignKey(Marca, on_delete=models.DO_NOTHING, related_name='produtos')
    criado = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name='produtos')
    empresa = models.ForeignKey(CNPJ, on_delete=models.DO_NOTHING, related_name='produtos')


