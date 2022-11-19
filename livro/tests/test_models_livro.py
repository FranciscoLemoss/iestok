from django.test import TestCase
from livro.models import Escola, Livro
from datetime import date
from django.utils import timezone


class EscolaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Escola.objects.create(descricao='Escola sacro-romana')

    def test_descricao_max_length(self):
        escola = Escola.objects.get(id=1)
        max_length = escola._meta.get_field('descricao').max_length
        self.assertEquals(max_length, 30, 'Atributo max_length do campo descrição do Model escola foi incorretamente definido')

    def test_descricao_label(self):
        escola = Escola.objects.get(id=1)
        descricao = escola._meta.get_field('descricao').verbose_name
        self.assertEquals(descricao, 'descrição', 'Label do campo descrição não foi corretamente configurado')

class LivroModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        escola = Escola.objects.create(descricao='Escola sacro-romana')
        Livro.objects.create(
            escola=escola,
            titulo='Senhor do anéis',
            autor='Charles Chapim',
            sinopse='Qualquer coisa',
            preco = 575.00,
        )

    def test_titulo_autor_max_length(self):
        livro = Livro.objects.get(id=1)
        max_length_titulo = livro._meta.get_field('titulo').max_length
        max_length_autor = livro._meta.get_field('autor').max_length
        self.assertEquals(max_length_titulo, 30, 'Limite de caracteres para o campo título da tabela Livro não configurado no banco de dados!')
        self.assertEquals(max_length_autor, 30, 'Limite de caracteres para o campo autor da tabela Livro não configurado no banco de dados!')

    def test_titulo_label(self):
        livro = Livro.objects.get(id=1)
        titulo = livro._meta.get_field('titulo').verbose_name
        self.assertEquals(titulo, 'título', 'Label do campo titulo do Model Livro não foi devidamente condigurado')

    def test_sinopse_label(self):
        livro = Livro.objects.get(id=1)
        sinopse = livro._meta.get_field('sinopse').verbose_name
        self.assertEquals(sinopse, 'sinópse', 'Label do campo sinopse do Model Livro não foi devidamente condigurado')

    def test_data_publicacao_label(self):
        livro = Livro.objects.get(id=1)
        data_publicacao = livro._meta.get_field('data_publicacao').default
        self.assertEquals(data_publicacao, timezone.now, 'Atributo default do campo data_publicacao do Model Livro não foi devidamente condigurado')

    def test_preco_label(self):
        livro = Livro.objects.get(id=1)
        preco = livro._meta.get_field('preco').default
        self.assertEquals(preco, 0, 'Atributo default do campo preco do Model Livro não foi devidamente configurado')
