from django.shortcuts import render
from .models import Filme

def index(request):
    filme = Filme.objects.all()
    print(type(filme))
    return render(request, 'filmes/index.html', {'filme': filme})