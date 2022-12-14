from django.db import models
from django.utils import timezone
# Create your models here.


class Escola(models.Model):
    descricao = models.CharField(verbose_name='descrição', null=False, max_length=30)
    def __str__(self):
        return self.descricao


class Livro(models.Model):
    escola = models.OneToOneField(Escola, on_delete=models.SET_NULL, null=True)
    titulo = models.CharField(verbose_name='título', null=False, max_length=30)
    autor = models.CharField(verbose_name='autor', null=False, max_length=30)
    sinopse = models.TextField(verbose_name='sinópse', null=False)
    data_publicacao = models.DateField(verbose_name='Data de publicação', null=False, default=timezone.now)
    preco = models.FloatField(verbose_name='Preço', null=False, default=0)


