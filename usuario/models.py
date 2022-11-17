from django.db import models
from livro.models import Escola
from django.contrib.auth.models import User


class Preferencias(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    preferencia = models.ForeignKey(Escola, on_delete=models.CASCADE)


