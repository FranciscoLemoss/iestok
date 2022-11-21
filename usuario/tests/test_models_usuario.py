from django.test import TestCase
from usuario.models import Preferencia
from django.contrib.auth.models import User
from livro.models import Escola
from django.db import models


"""class Preferencias(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    preferencia = models.ForeignKey(Escola, on_delete=models.CASCADE)"""

class PreferenciaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        usuario = User.objects.create_user(username='fr.lemos@yahoo.com.br',
                                    email='fr.lemos@yahoo.com.br',
                                    first_name='Francisco',
                                    password='francisco123')
        escola = Escola.objects.create(descricao='Escola sacro-romana')
        Preferencia.objects.create(usuario=usuario, escola=escola)

    def test_preferencia_usuario_escola(self):
        preferencia = Preferencia.objects.get(id=1)
        usuario = preferencia.usuario
        escola = preferencia.escola
        self.assertEquals(usuario.first_name, 'Francisco', 'A preferência não está sendo associada ao usuário')
        self.assertEquals(escola.descricao, 'Escola sacro-romana', 'A preferência não está sendo associada ao usuário')

    def test_on_delete_cascade(self):
        usuario = User.objects.get(id=1)
        usuario.delete()
        preferencias = Preferencia.objects.all()
        self.assertTrue(len(preferencias) == 0, 'O atributo ondelete do campo usuário no model Preferencias não foi devidamente configurado')


    def test_escola_delete_cascade(self):
        escola = Escola.objects.get(id=1)
        escola.delete()
        preferencias = Preferencia.objects.all()
        self.assertTrue(len(preferencias) == 0,
                        'O atributo ondelete do campo escola no model Preferencias não foi devidamente configurado')
