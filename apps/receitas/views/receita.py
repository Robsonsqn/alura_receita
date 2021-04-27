from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from receitas.models import Receita


# Create your views here.
def index(request):
    '''
        Redirect to a main page
    '''
    receitas = Receita.objects.filter(publicada=True).order_by('-data_receita')
    paginator = Paginator(receitas, 6)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)
    dados = {
        'receitas' : receitas_por_pagina
    }
    return render(request, 'receitas/index.html', dados)


def receita(request, receita_id):
    '''
        Details of an recipe
    '''
    receita_a_exibir = {
        'receita' : get_object_or_404(Receita, pk=receita_id)
    }
    return render(request, 'receitas/receita.html', receita_a_exibir)


def cria_receita (request):
    '''
        Create a new Recipe in system
    '''
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        if _campo_vazio(nome_receita) or _campo_vazio(ingredientes):
            messages.error(request, "Os campos nome da receita e ingredientes não podem ser nulos")
            return redirect('cria_receita')
        if _campo_vazio(modo_preparo) or _campo_vazio(tempo_preparo):
            messages.error(request, "Os campos tempo e modo de preparo não podem ser nulos")
            return redirect('cria_receita')
        if _campo_vazio(rendimento) or _campo_vazio(categoria):
            messages.error(request, "Os campos rendimento e categoria não podem ser nulos")
            return redirect('cria_receita')
        user = get_object_or_404(User, pk=request.user.id)
        new_receita = Receita.objects.create(
            pessoa=user, nome_receita=nome_receita, 
            ingredientes=ingredientes, modo_preparo=modo_preparo, 
            tempo_preparo=tempo_preparo, rendimento=rendimento, 
            categoria=categoria, foto_receita=foto_receita)
        new_receita.save()
        return redirect('dashboard')
    else:
        return render(request,'receitas/cria_receita.html')


def deleta_receita(request, receita_id):
    '''
        Delete an recipe by id
    '''
    removed_receita = get_object_or_404(Receita, pk=receita_id)
    removed_receita.delete()
    messages.success(request, 'Receita deletada com sucesso')
    return redirect('dashboard')


def edita_receita(request, receita_id):
    '''
        Go to page "Edita_receita"
    '''
    edited_receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = {
        'receita' : edited_receita
    }
    return render(request, 'receitas/edita_receita.html', receita_a_editar)


def atualiza_receita(request):
    '''
        Update an recipe by object
    '''
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        if _campo_vazio(receita_id):
            messages.error(request, 'Receita não pode ser nula')
            return redirect('dashboard')
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        if _campo_vazio(nome_receita) or _campo_vazio(ingredientes):
            messages.error(request, "Os campos nome da receita e ingredientes não podem ser nulos")
            return redirect('dashboard')
        if _campo_vazio(modo_preparo) or _campo_vazio(tempo_preparo):
            messages.error(request, "Os campos tempo e modo de preparo não podem ser nulos")
            return redirect('dashboard')
        if _campo_vazio(rendimento) or _campo_vazio(categoria):
            messages.error(request, "Os campos rendimento e categoria não podem ser nulos")
            return redirect('dashboard')
        old_receita = Receita.objects.get(pk=receita_id)
        old_receita.nome_receita = request.POST['nome_receita']
        old_receita.ingredientes = request.POST['ingredientes']
        old_receita.tempo_preparo = request.POST['tempo_preparo']
        old_receita.modo_preparo = request.POST['modo_preparo']
        old_receita.rendimento = request.POST['rendimento']
        old_receita.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            old_receita.foto_receita = request.FILES['foto_receita']
        old_receita.save()
        messages.success(request, 'Receita editada com sucesso')
        return redirect('dashboard')
    else :
        return redirect('dashboard')


def _campo_vazio(campo):
    return not campo.strip()
