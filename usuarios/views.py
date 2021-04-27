from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User 
from django.contrib import auth, messages
from receitas.models import Receita


def cadastro (request):
    '''
        Create new user based in a form
    '''
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if _campo_vazio(nome):
            messages.error(request, 'O nome não pode estar em branco')
            return redirect('cadastro')
        if _campo_vazio(email):
            messages.error(request, 'O email não pode estar em branco')
            return redirect('cadastro')
        if _campo_vazio(senha):
            messages.error(request, 'A senha não pode estar em branco')
            return redirect('cadastro')
        if senha != senha2:
            messages.error(request, 'As senhas não conhecidem')
            return redirect('cadastro')
        if _verifica_email(email):
            messages.error(request, 'Este email já esta em nosso sistema')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Este usuario já esta em nosso sistema')
            return redirect('cadastro')
        user = User.objects.create_user(username= email,email = email, password = senha, first_name=nome)
        user.save()
        messages.success(request, 'Cadastro realizado com sucesso')
        return redirect('login')
    else :
        return render(request, 'usuarios/cadastro.html')


def login (request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if _campo_vazio(email) or _campo_vazio(senha):
            messages.error(request, 'Os campos email e senha não podem ficar em branco')
            return redirect('login')
        if _verifica_email(email):
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    else:
        return render(request, 'usuarios/login.html')


def logout (request):
    auth.logout(request)
    return redirect('index')


def dashboard (request):
    if request.user.is_authenticated:
        user = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=user)

        dados = {
            'receitas' : receitas
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('login')


def _campo_vazio(campo):
    return not campo.strip()


def _verifica_email(email):
    return User.objects.filter(email = email).exists()
