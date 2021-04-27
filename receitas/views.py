from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User 
from .models import Receita


# Create your views here.
def index(request):
    receitas = Receita.objects.filter(publicada=True).order_by('-data_receita')

    dados = {
        'receitas' : receitas
    }
    return render(request, 'receitas/index.html', dados)


def receita(request, receita_id):
    receita_a_exibir = {
        'receita' : get_object_or_404(Receita, pk=receita_id)
    }
    return render(request, 'receitas/receita.html', receita_a_exibir)


def buscar(request):
    lista_receitas = Receita.objects.filter(publicada=True).order_by('-data_receita')

    if ('buscar' in request.GET):
        nome_a_buscar = request.GET['buscar']
        if (nome_a_buscar):
            lista_receitas = Receita.objects.filter(nome_receita__icontains=nome_a_buscar, publicada=True).order_by('-data_receita')
    dados = {
        'receitas' : lista_receitas
    }
    return render(request, 'receitas/buscar.html', dados)


def cria_receita (request):
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        if _campo_vazio(nome_receita):
            messages.error(request, "O campo nome da receita não pode ser nulo")
            return redirect('cria_receita')
        if _campo_vazio(ingredientes):
            messages.error(request, "O campo ingredientes não pode ser nulo")
            return redirect('cria_receita')
        if _campo_vazio(modo_preparo):
            messages.error(request, "O campo modo de preparo não pode ser nulo")
            return redirect('cria_receita')
        if _campo_vazio(tempo_preparo):
            messages.error(request, "O campo tempo de preparo não pode ser nulo")
            return redirect('cria_receita')
        if _campo_vazio(rendimento):
            messages.error(request, "O campo rendimento não pode ser nulo")
            return redirect('cria_receita')
        if _campo_vazio(categoria):
            messages.error(request, "O campo categoria não pode ser nulo")
            return redirect('cria_receita')
        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes, modo_preparo=modo_preparo, tempo_preparo=tempo_preparo, rendimento=rendimento, categoria=categoria, foto_receita=foto_receita)
        receita.save()
        return redirect('dashboard')
    else:
        return render(request,'receitas/cria_receita.html')


def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    messages.success(request, 'Receita deletada com sucesso')
    return redirect('dashboard')


def edita_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = {
        'receita' : receita
    }
    return render(request, 'receitas/edita_receita.html', receita_a_editar)


def atualiza_receita(request):
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        if _campo_vazio(receita_id):
            messages.error(request, 'Receita não pode ser nula')
            return redirect('dashboard')
        if _campo_vazio(request.POST['nome_receita']):
            messages.error(request, 'O campo nome da receita não pode ser nulo')
            return redirect('dashboard')
        if _campo_vazio(request.POST['ingredientes']):
            messages.error(request, 'O campo ingredientes não pode ser nulo')
            return redirect('dashboard')
        if _campo_vazio(request.POST['categoria']):
            messages.error(request, 'O campo categoria não pode ser nulo')
            return redirect('dashboard')
        if _campo_vazio(request.POST['rendimento']):
            messages.error(request, 'O campo rendimento não pode ser nulo')
            return redirect('dashboard')
        if _campo_vazio(request.POST['modo_preparo']):
            messages.error(request, 'O campo modo preparo não pode ser nulo')
            return redirect('dashboard')
        if _campo_vazio(request.POST['tempo_preparo']):
            messages.error(request, 'O campo tempo preparo não pode ser nulo')
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


def _campo_vazio(campo):
    return not campo.strip()
