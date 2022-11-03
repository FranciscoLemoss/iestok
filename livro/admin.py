from django.contrib import admin

# Register your models here.

from .models import Escola, Livro

# Register your models here.

class EscolaAdmin(admin.ModelAdmin):
    list_display = ('descricao', )

class LivroAdmin(admin.ModelAdmin):
    list_display = ('escola', 'titulo', 'autor', 'sinopse', 'data_publicacao')

admin.site.register(Escola, EscolaAdmin)
admin.site.register(Livro, LivroAdmin)

