from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from usuario.models import Preferencia
from livro.models import Escola


class PreferenciasViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        numero_escolas = 10
        for num_escola in range(numero_escolas):
            Escola.objects.create(
                descricao=f'escola n° {num_escola}',
            )
        user = User.objects.create_user(username='Francisco',
                                        email='francisco@gmail.com',
                                        first_name='Francisco',
                                        password='francisco123')
        user.save()

    def test_view_url_existe_e_responde(self):
        response = self.client.get('/cadastro/')
        self.assertEqual(response.status_code, 200, 'Endereço /cadastro indisponível')
        response = self.client.get('/congratulations/')
        self.assertEqual(response.status_code, 302, 'Endereço /congratulations não redireciona quando sem login')
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200, 'Endereço /login indisponível')
        response = self.client.get('/catalogo')
        self.assertEqual(response.status_code, 302, 'Endereço /catalogo não redireciona quando sem login')

    def test_view_url_existe_e_responde_atributo_name(self):
        response = self.client.get(reverse('cadastro'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('congratulations'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('catalogo'))
        self.assertEqual(response.status_code, 302)

    def test_view_usa_template_correto(self):
        response = self.client.get(reverse('cadastro'))
        self.assertTemplateUsed(response, 'usuario/cadastro.html', 'A url cadastro não está renderizando a página cadastro.html')
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'usuario/login.html', 'A url login não está renderizando a página login.html')

    def test_view_redireciona_correto(self):
        self.client.login(username='Francisco', password='francisco123')
        response = self.client.get(reverse('cadastro'))
        self.assertEqual(response.status_code, 302, 'A url cadastro não está respondendo com redirecionamento quando o usuário está logado')
        self.assertRedirects(response, '/congratulations/')

        response = self.client.get(reverse('sair'))
        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='Francisco', password='francisco123')
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/congratulations/')
        self.assertEqual(response.status_code, 302)

        escolas = Escola.objects.all()
        usuario = User.objects.get(username='Francisco')
        for escola in escolas:
            preferencia = Preferencia.objects.create(
                usuario=usuario,
                escola=escola,
            )
            preferencia.save()

        self.client.login(username='Francisco', password='francisco123')
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/catalogo')
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('congratulations'))
        self.assertRedirects(response, '/catalogo')
        self.assertEqual(response.status_code, 302)

    def test_login_error(self):
        login = self.client.login(username='Francisco', password='francisco12')
        self.assertFalse(login, 'Falha na realização de login.')
