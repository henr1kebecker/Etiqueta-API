from .models import Usuario, Produto, Marca
from .serializers import UserSerializer, PontoSerializer
from rest_framework import permissions, viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .serializers import (LoginSerializer, UsuarioData, MarcaSerializer, 
                          ProdutoSerializer, MarcaListaSerializer, ProdutoListaSerializer)
from rest_framework.views import APIView
from django.views.decorators.csrf import get_token
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


def getToken(request):
    token = get_token(request)
    
    return JsonResponse({'token': token})


@api_view(['POST'])
@permission_classes([AllowAny])
def verificar_token(request):
    token = request.data.get('toke')

    if not token:
        return Response({'detail': 'Token não fornecido'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        toke = AccessToken(token)
        return Response({'token': True}, status=status.HTTP_200_OK)

    except TokenError as e:
        if isinstance(e, TokenError) and e.args[0] == 'Token is invalid or expired':
            print(e.args)
            return Response({'token': False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print('falso')
            print('Erro: ', e.args[0])
            return Response({'token': False}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    act = request.data.get('refresh')
    print(act)
    if not act:
        return Response({'detail': 'Token de atualização não fornecido'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        refresh_tk = RefreshToken(act)
        new_refresh = refresh_tk.access_token
        return Response({'acess':str(new_refresh)}, status=status.HTTP_200_OK)
    except TokenError as e:
        return Response({'detail':'Tokend de atualização inválido ou expirado!'}, status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        dt = user.data()
        print(dt)
        return Response({'acesso':True, 'user': dt})
        

class JustificarPonto(generics.CreateAPIView):
    authentication_classes= ()
    serializer_class = PontoSerializer
    permission_classes = [IsAuthenticated]


class CriarMarca(generics.CreateAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [IsAuthenticated]


class ListaMarca(generics.ListAPIView):
    
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
    serializer_class = MarcaSerializer
    permission_classes = [IsAuthenticated]


class CriarProduto(generics.CreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]


class ListaProdutos(generics.ListAPIView):
    
    serializer_class = ProdutoListaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Produto.objects.all()
        buscar = self.request.query_params.get('nome', None)

        if buscar:
            queryset = queryset.filter(nome__icontains=buscar).order_by('nome')
            # data = self.serializer_class(lista, many=True)
            return queryset
    
        return queryset.order_by('nome')


class UpdateProdutos(generics.UpdateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]