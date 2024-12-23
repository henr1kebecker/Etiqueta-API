from .models import Usuario, Produto, Marca
from .serializers import UserSerializer, PontoSerializer
from rest_framework import permissions, viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .serializers import (LoginSerializer, MarcaSerializer, 
                          ProdutoSerializer, MarcaListaSerializer, ProdutoListaSerializer)
from rest_framework.views import APIView
from django.views.decorators.csrf import get_token
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

def getToken(request):
    token = get_token(request)

    
    return JsonResponse({'token': token})


@api_view(['POST'])
@permission_classes([AllowAny])
def checkToken(request):
    token = request.headers.get('Authorization')

    if token is not None:
        try:
            token_key = token.split(' ')[1]
        except IndexError:
            return Response({'error': 'Token Invalido!'} ,status=status.HTTP_400_BAD_REQUEST)

        try:
            tk = Token.objects.get(key=token_key)
            return Response({'acesso': True, 'token': 'Válido'})
        except Token.DoesNotExist:
            return Response({'acesso': False, 'error': 'Token inválido!'})
        

class UserViewSet(viewsets.ModelViewSet):

    queryset = Usuario.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegistrarUser(generics.CreateAPIView):
    authentication_classes= ()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    

class LoginToken(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        codigo = request.data.get('codigo')
        pwd = request.data.get('password')
        
        user = authenticate(codigo=codigo, password=pwd)
        data = { 'nome': user.nome, 'setor': user.setor }

        if user is not None:
            token, criar = Token.objects.get_or_create(user=user)
            return Response({'acesso':True, 'token': token.key, 'usuario': data})
        else:
            return Response({'acesso':False, 'erro': 'Codigo e/ou senha inválidos' })



class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        tk = Token.objects.get(user=user)
        tk.delete()
        return Response({'msg': 'Token deletado!'})

class JustificarPonto(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = PontoSerializer
    permission_classes = [IsAuthenticated]


class CriarMarca(generics.CreateAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)


class ListaMarca(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = MarcaListaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Marca.objects.all()
        buscar = self.request.query_params.get('nome', None)

        if buscar:
            queryset = queryset.filter(marca__icontains=buscar).order_by('marca')
            # data = self.serializer_class(lista, many=True)
            return queryset
    
        return queryset.order_by('marca')
        

class EditarMarca(generics.UpdateAPIView):
    queryset = Marca.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = MarcaSerializer
    permission_classes = [IsAuthenticated]


class CriarProduto(generics.CreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)


class ListaProdutos(generics.ListAPIView):

    authentication_classes = (TokenAuthentication,)
    serializer_class = ProdutoListaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Produto.objects.all()
        buscar = self.request.query_params.get('nome', None)
        id = self.request.query_params.get('id', None)

        if buscar:
            queryset = queryset.filter(nome__icontains=buscar).order_by('nome')
            # data = self.serializer_class(lista, many=True)
            return queryset
        if id:
            id = int(id)
            queryset = queryset.filter(id=id)
            # data = self.serializer_class(lista, many=True)
            return queryset

    
        return queryset.order_by('nome')


class UpdateProdutos(generics.UpdateAPIView):

    authentication_classes = (TokenAuthentication,)
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]