from django.urls import path
from . import views

urlpatterns = [
    # path('', views.Index.as_view(), name='index'),
    path('<int:id_filmes>', views.detalhe, name='detalhe'),
    path('', views.index, name='index'),
    path('busca/', views.busca, name='busca'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('cadastro', views.cadastro, name='cadastro')
]
