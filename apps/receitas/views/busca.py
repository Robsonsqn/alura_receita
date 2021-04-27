from django.shortcuts import render
from receitas.models import Receita


def busca(request):
    lista_receitas = Receita.objects.filter(publicada=True).order_by('-data_receita')

    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        lista_receitas = Receita.objects.filter(nome_receita__icontains=nome_a_buscar, publicada=True).order_by('-data_receita')
    
    dados = {
        'receitas' : lista_receitas
    }
    return render(request, 'receitas/buscar.html', dados)
