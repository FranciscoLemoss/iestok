from django.test import TestCase
from usuario.models import Preferencia
from django.contrib.auth.models import User
from livro.models import Escola

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


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='fr.lemos@yahoo.com.br',
                                    email='fr.lemos@yahoo.com.br',
                                    first_name='Francisco',
                                    password='francisco123')
    def test_email_label(self):
        usuario = User.objects.get(id=1)
        email = usuario.email
        self.assertEquals(email, 'fr.lemos@yahoo.com.br', 'O campo email não está sendo associado ao usuário correspondente')

    def test_first_name_label(self):
        usuario = User.objects.get(id=1)
        first_name = usuario.first_name
        self.assertEquals(first_name, 'Francisco', 'O campo nome não está sendo vinculado ao usuário correspondente ')