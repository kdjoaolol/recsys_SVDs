from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from .models import Filme
from django.core.paginator import Paginator
import numpy as np
import pandas as pd
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.contrib.auth.models import User
from .models import Rating
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds


@login_required(login_url='login')
def index(request):
    try:
        df_ratings = pd.DataFrame(Rating.objects.values())
        df_ratings.drop_duplicates(subset=['id_usuario', 'id_filme'], keep='last', inplace=True)
        df_ratings_pivot = df_ratings.pivot(index='id_usuario', values='rating', columns='id_filme').fillna(2.5)
        users_items_pivot_matrix = csr_matrix(df_ratings_pivot.values)
        users_ids = list(df_ratings_pivot.index)
        U, sigma, Vt = svds(users_items_pivot_matrix, k = 25)
        sigma = np.diag(sigma)
        all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) 
        cf_preds_df = pd.DataFrame(all_user_predicted_ratings, columns = df_ratings_pivot.columns, index=users_ids).T
        recomendacoes_personalizadas = cf_preds_df[str(auth.get_user(request))]
        filmes_vistos = df_ratings.loc[df_ratings['id_usuario'] == str(auth.get_user(request)), 'id_filme'].values
        filme = Filme.objects.values('id_filmes','urls_imgs_185')
        filmes_score = []

        for dicts in filme:
            if not dicts['id_filmes'] in filmes_vistos:
                dicts.update({'score': recomendacoes_personalizadas[dicts['id_filmes']]})
                filmes_score.append(dicts)
        filmes_score = sorted(filmes_score, key=lambda d: d['score'], reverse=True) 

    except KeyError:
        filmes_score = Filme.objects.all()
    paginator = Paginator(filmes_score, 12)
    page = request.GET.get('p')
    filmes_score = paginator.get_page(page)
    
    return render(request, 'filmes/index.html', {'filmes': filmes_score})


@login_required(login_url='login')
def detalhe(request, id_filmes):
    filme = get_object_or_404(Filme, id_filmes=id_filmes)
    if request.method == 'POST':
        ratings = Rating(id_usuario=auth.get_user(request), rating=request.POST.get('rate'), id_filme=filme.id_filmes)
        ratings.save()
        return redirect('index')
    return render(request, 'filmes/detalhes.html', {'filme': filme})

def busca(request):
    termo = request.GET.get('termo')
    filme = Filme.objects.order_by('-id_filmes').filter(Q(title__icontains=termo) | Q(overview__icontains=termo))
    paginator = Paginator(filme, 24)
    page = request.GET.get('p')
    filme = paginator.get_page(page)
    return render(request, 'filmes/index.html', {'filmes': filme})


def login(request):
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        return render(request, 'filmes/login.html')

    auth.login(request, user)

    return redirect('index')

def logout(request):
    auth.logout(request)
    return redirect('login')

def cadastro(request):

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        # messages.error(request, 'Nenhum campo pode estar vazio')
        return render(request, 'filmes/cadastro.html')
    
    try:
        validate_email(email)
    except:
        return render(request, 'filmes/cadastro.html')

    if len(senha) < 6:
        return render(request, 'filmes/cadastro.html')

    if len(usuario) < 6:
        return render(request, 'filmes/cadastro.html')

    if senha != senha2:
        return render(request, 'filmes/cadastro.html')
    
    if User.objects.filter(username=usuario).exists():
        return render(request, 'filmes/cadastro.html')

    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()

    return redirect('login')