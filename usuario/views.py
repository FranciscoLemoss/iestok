from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user, logout
from livro.models import Escola
from .models import Preferencias
# Create your views here.

def index(request):

    user = get_user(request)

    if user.is_authenticated:
        preferencias = Preferencias.objects.filter(usuario=user)
        if preferencias:
            return redirect('catalogo')
        else:
            return redirect('congratulations')

    return render(request, 'usuario/index.html')

def cadastro(request):

    user = get_user(request)

    if user.is_authenticated:
        return redirect('congratulations')

    if request.method != 'POST':
        return render(request, 'usuario/cadastro.html')

    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha_repetida = request.POST.get('senha_repetida')
    
    if nome:
        username = nome.lower()
    else:
        messages.add_message(request, messages.ERROR, 'Todos os campos devem ser preenchidos!')
        return render(request, 'usuario/cadastro.html')

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

    try:
        User.objects.create_user(username=email,
                                    email=email,
                                    first_name=nome.title(),
                                    password=senha)
    except:
        messages.add_message(request, messages.ERROR, 'Tente outro nome de usuário!')
        return render(request, 'usuario/cadastro.html')


    messages.add_message(request, messages.SUCCESS, 'Cadastro efetivado com sucesso!')
    user = auth.authenticate(request, username=email, password=senha)
    auth.login(request, user)
    return redirect('congratulations')

def login(request):

    user = get_user(request)

    if user.is_authenticated:
        preferencias = Preferencias.objects.filter(usuario=user)
        if preferencias:
            return redirect('catalogo')
        else:
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
        preferencias = Preferencias.objects.filter(usuario=user)
        if preferencias:
            return redirect('catalogo')
        else:
            return redirect('congratulations')
        messages.add_message(request, messages.SUCCESS, 'Você fez login com sucesso!')
        return redirect('congratulations')


@login_required(redirect_field_name='login')
def congratulations(request):

    user = get_user(request)

    if user.is_authenticated:
        preferencias = Preferencias.objects.filter(usuario=user)
        if len(preferencias) > 0:
            return redirect('catalogo')

    escolas = Escola.objects.order_by('id')
    if request.method != 'POST':
        return render(request, 'usuario/congratulations.html', {'escolas':escolas})

    for escola in escolas:
        checkbox = request.POST.get(escola.descricao)
        if checkbox:
            preferencia = Preferencias()
            preferencia.usuario = user
            preferencia.preferencia = escola
            preferencia.save()

    return redirect('catalogo')


def sair(request):

    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout realizado com sucesso!')
    return redirect('index')
