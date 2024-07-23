from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UsuarioManager(BaseUserManager):
    def create_user(self, codigo, nome, setor, password, password1, **extra_fields):
        if not codigo:
            raise ValueError(_('Código é obrigatório'))
        if not nome:
            raise ValueError(_('Nome é obrigatório'))
        if password != password1:
            raise ValueError(_('As senhas precisam ser iguais.'))
    

        user = self.model(codigo=codigo, **extra_fields)
        user.nome = nome
        user.setor = setor
        user.set_password(password)
        user.save(using=self._db)
        return user
