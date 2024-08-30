from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Usuario(AbstractUser):
    CARGO = (
        ('ADM', 'Administrativo'),
        ('LD', 'Lider'),
        ('USER', 'Operacional')
    )

    username = models.CharField(max_length=10, unique=False, blank=True, null=True, default="")
    codigo = models.CharField(_("Codigo"), unique=True, max_length=4)
    nome = models.CharField(_('Nome'), max_length=20)
    setor = models.CharField(_('Setor'), max_length=15, choices=CARGO, default='USER')



    USERNAME_FIELD = 'codigo'
    REQUIRED_FIELDS = ['nome']

    # objects = UsuarioManager()

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

    

class Marca(models.Model):
    marca = models.CharField(max_length=30, verbose_name='Marca')
    criado = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name='marcas')

    def __str__(self)-> str:
        return self.marca


class Produto(models.Model):
    nome = models.CharField(max_length=30, verbose_name='Produto')
    marca = models.ForeignKey(Marca, on_delete=models.DO_NOTHING, related_name='produtos')
    criado = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name='produtos')


class CNPJ(models.Model):
    razao_social = models.CharField(max_length=50, blank=False, null=False, verbose_name='Razão Social')
    nome_fantasia = models.CharField(max_length=50, blank=False, null=False, verbose_name='Nome Fantasia')
    cnpj = models.CharField(max_length=14, blank=False, null=False, verbose_name='CNPJ')
    criado = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name='cnpjs')