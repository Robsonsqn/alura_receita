from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Receita

# Create your views here.
def index(request):
    receitas = Receita.objects.filter(publicada=True).order_by('-data_receita')

    dados = {
        'receitas' : receitas
    }
    return render(request, 'index.html', dados)

def receita(request, receita_id):
    receita_a_exibir = {
        'receita' : get_object_or_404(Receita, pk=receita_id)
    }
    return render(request, 'receita.html', receita_a_exibir)

def buscar(request):
    lista_receitas = Receita.objects.filter(publicada=True).order_by('-data_receita')

    if ('buscar' in request.GET):
        nome_a_buscar = request.GET['buscar']
        if (nome_a_buscar):
            lista_receitas = Receita.objects.filter(nome_receita__icontains=nome_a_buscar, publicada=True).order_by('-data_receita')
    dados = {
        'receitas' : lista_receitas
    }
    return render(request, 'buscar.html', dados)
