from django.urls import path
from app import views as v


urlpatterns = [
    path('login/', v.LoginToken.as_view(), name='login'),
    path('logout/', v.Logout.as_view(), name='logout'),
    path('check-token/', v.checkToken, name='CheckToken'),
    path('criar/', v.RegistrarUser.as_view(), name='criarConta'),
    path('pj/editar/<int:pk>/', v.EditarPj.as_view(), name='EditarConta'),
    path('get-token/', v.getToken, name='getToken'),
    path('justificar-ponto/', v.JustificarPonto.as_view(), name='VerificarToken'),
    path('marca/', v.ListaMarca.as_view(), name='ListarMarca'),
    path('marca/criar/', v.CriarMarca.as_view(), name='CriarMarca'),
    path('marca/editar/<int:pk>/', v.EditarMarca.as_view(), name='EditarMarca'),
    path('produto/', v.ListaProdutos.as_view(), name='ListaProdutos'),
    path('produto/novo/', v.CriarProduto.as_view(), name='CriarProduto'),
    path('produto/editar/<int:pk>/', v.UpdateProdutos.as_view(), name='EditarProdutos'),
    path('instituicao/criar/', v.PessoaJuridica.as_view(), name='Instituicao'),
]
