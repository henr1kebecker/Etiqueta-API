from django.urls import path
from app import views as v
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('login/', v.LoginToken.as_view(), name='login'),
    path('criar/', v.RegistrarUser.as_view(), name='criarConta'),
    path('get-token/', v.getToken, name='getToken'),
    path('login-token/', TokenObtainPairView.as_view(), name='loginToken'),
    path('refresh-token/', v.refresh_token, name='refreshToken'),
    path('validar-token/', v.verificar_token, name='VerificarToken'),
    path('justificar-ponto/', v.JustificarPonto.as_view(), name='VerificarToken'),
    path('marca/', v.ListaMarca.as_view(), name='ListarMarca'),
    path('marca/criar/', v.CriarMarca.as_view(), name='CriarMarca'),
    path('marca/editar/<int:pk>/', v.EditarMarca.as_view(), name='EditarMarca'),
    path('produto/', v.ListaProdutos.as_view(), name='ListaProdutos'),
    path('produto/novo/', v.CriarProduto.as_view(), name='CriarProduto'),
    path('produto/editar/<int:pk>/', v.UpdateProdutos.as_view(), name='EditarProdutos'),
]
