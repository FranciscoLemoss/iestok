from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user, logout
# Create your views here.

def index(request):

    user = get_user(request)

    if user.is_authenticated:
        return redirect('congratulations')

    return render(request, 'usuario/index.html')

def cadastro(request):

    user = get_user(request)

    if user.is_authenticated:
        return redirect('congratulations')

    if request.method != 'POST':
        return render(request, 'usuario/cadastro.html')

    username = request.POST.get('username')
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha_repetida = request.POST.get('senha_repetida')
    print(nome)

    if not username or not nome or not email or not senha or not senha_repetida:
        messages.add_message(request, messages.ERROR, 'Todos os campos devem ser preenchidos!')
        return render(request, 'usuario/cadastro.html')

    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.ERROR, 'Email inválido!')
        return render(request, 'usuario/cadastro.html')

    if len(nome.strip()) < 4:
        messages.add_message(request, messages.ERROR, 'Inclua o nome completo.')
        return render(request, 'usuario/cadastro.html')

    if len(username.strip()) < 4:
        messages.add_message(request, messages.ERROR, 'Digite um nome de usuário com no mínimo 5 dígitos.')
        return render(request, 'usuario/cadastro.html')

    if len(senha) < 8:
        messages.add_message(request, messages.ERROR, 'A senha deve ter no mínimo 8 dígitos!')
        return render(request, 'usuario/cadastro.html')

    if senha != senha_repetida:
        messages.add_message(request, messages.ERROR, 'As Senhas não são iguais!')
        return render(request, 'usuario/cadastro.html')

    if User.objects.filter(email=email):
        messages.add_message(request, messages.ERROR, 'Email já está cadastrado!')
        return render(request, 'usuario/cadastro.html')

    User.objects.create_user(username=username,
                                    email=email,
                                    first_name=nome,
                                    password=senha)

    messages.add_message(request, messages.SUCCESS, 'Cadastro efetivado com sucesso!')

    return render(request, 'usuario/congratulations.html', {'nome': nome})

def login(request):

    user = get_user(request)


    if user.is_authenticated:
        return redirect('congratulations')

    if request.method != 'POST':
        return render(request, 'usuario/login.html')

    email = request.POST.get('email')
    email = email.strip()

    senha = request.POST.get('senha')
    senha = senha.strip()

    if not email or not senha:
        messages.add_message(request, messages.ERROR, 'Forneça o email e senha para login!')
        return render(request, 'usuario/login.html')

    try:
        user = get_object_or_404(User, email=email)
    except:
        messages.add_message(request, messages.ERROR, 'Email inválido!')
        return render(request, 'usuario/login.html')

    user = auth.authenticate(request, username=user.username, password=senha)

    if not user:
        messages.add_message(request, messages.ERROR, 'Usuário ou senha inválidos!')
        return render(request, 'usuario/login.html')
    else:
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Você fez login com sucesso!')
        return redirect('congratulations')


@login_required(redirect_field_name='login')
def congratulations(request):
    return render(request, 'usuario/congratulations.html')

def sair(request):

    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout realizado com sucesso!')
    return redirect('index')
