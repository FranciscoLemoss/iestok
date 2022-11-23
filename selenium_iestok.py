from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import random

class ChromeAuto:
    def __init__(self):
        self.driver_path = 'chromedriver'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('user-data-dir=C:/Usuários/Francisco/AppData/Local/Google/Chrome/User Data')
        self.chrome = webdriver.Chrome(
            self.driver_path,
            options=self.options
        )

    def clica_entrar(self):
        try:
            btn_entrar = self.chrome.find_element(By.ID, 'botao_entrar_2')
            btn_entrar.click()
        except Exception as e:
            print('Erro ao clicar no botão entrar', e)

    def clica_cadastrar(self):
        try:
            btn_cadastrar = self.chrome.find_element(By.ID, 'botao_cadastrar')
            btn_cadastrar.click()
        except Exception as e:
            print('Erro ao clicar no botão cadastrar', e)

    def realizar_login(self, email, senha):
        try:
            input_email = self.chrome.find_element(By.NAME, 'email')
            input_email.send_keys(email)
            input_senha = self.chrome.find_element(By.NAME, 'senha')
            input_senha.send_keys(senha)
            sleep(1)
            btn_efetivar_login = self.chrome.find_element(By.ID, 'efetivar_login')
            btn_efetivar_login.click()
            sleep(1)
            if 'catalogo' not in self.chrome.current_url:
                print(f'Erro: Página de catálogo não acessada pelo usuário de email {email}! Verificar se de fato foi atribuída'
                      f' preferência ao usuário.')
            btn_sair = self.chrome.find_element(By.ID, 'botao_sair')
            btn_sair.click()
        except Exception as e:
            print(f'Erro ao efetivar o cadastro do usuário de email {email} e senha {senha}, reinicie a operação :', e)

    def preencher_cadastro(self, nome, email, senha):
        try:
            input_nome = self.chrome.find_element(By.NAME, 'nome')
            input_nome.send_keys(nome)
            input_email = self.chrome.find_element(By.NAME, 'email')
            input_email.send_keys(email)
            input_senha = self.chrome.find_element(By.NAME, 'senha')
            input_senha.send_keys(senha)
            input_senha_repetida = self.chrome.find_element(By.NAME, 'senha_repetida')
            input_senha_repetida.send_keys(senha)
            sleep(1)
            btn_efetivar_cadastro = self.chrome.find_element(By.ID, 'efetivar_cadastro')
            btn_efetivar_cadastro.click()
            sleep(1)
            try:
                lista_preferencias = ('Metafísica platônica', 'Conselhos financeiros', 'Sabedoria dos sofistas', 'Administração financeira')
                index_qualquer = random.randint(0,3)
                check_preferencia = self.chrome.find_element(By.ID, lista_preferencias[index_qualquer])
                check_preferencia.click()
                sleep(1)
                btn_enviar_preferencias = self.chrome.find_element(By.ID, 'enviar_preferencias')
                btn_enviar_preferencias.click()
                sleep(1)
                btn_sair = self.chrome.find_element(By.ID, 'botao_sair')
                btn_sair.click()
            except Exception as e:
                print(f'Usuário {nome} já cadastrado no banco de dados, delete o registro para fazer o teste:', e)
        except Exception as e:
            print(f'Erro ao cadastrar o usuário de nome {nome} in:', e)

    def acessa(self, site):
        self.chrome.get(site)

    def sair(self):
        self.chrome.quit()


if __name__ == '__main__':

    lista_usuarios = [
        ('maria_0', 'maria_0@gmail.com', 'maria_023'),
    ]
    for num in range(1, 10):
        nome = lista_usuarios[0][0].replace('0', str(num))
        email = lista_usuarios[0][1].replace('0', str(num))
        senha = lista_usuarios[0][2].replace('0', str(num))
        lista_usuarios.append((nome, email, senha))

    chrome = ChromeAuto()
    chrome.acessa('http://127.0.0.1:8000/')

    for usuario in lista_usuarios:
        chrome.clica_cadastrar()
        sleep(1)
        chrome.preencher_cadastro(usuario[0], usuario[1], usuario[2])

    sleep(3)
    chrome.clica_entrar()

    for usuario in lista_usuarios:
        chrome.clica_entrar()
        sleep(1)
        chrome.realizar_login(usuario[1], usuario[2])

    chrome.sair()
