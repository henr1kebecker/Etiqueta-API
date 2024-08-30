from .models import Usuario, Ponto
from rest_framework import serializers
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login
from .models import Usuario, Marca, Produto, CNPJ
from unidecode import unidecode


class UserSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(
        label="Senha",
        write_only=True, 
        style={'input_type': 'password'},
        trim_whitespace=False,
    )
    senha2 = serializers.CharField(
        label="Repita a Senha",
        write_only=True, 
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    class Meta:
        model = Usuario
        fields = ['codigo','nome', 'setor', 'senha', 'senha2']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        user = Usuario(
            codigo=self.validated_data['codigo'],
            nome=self.validated_data['nome'],
            setor=self.validated_data['setor'],
        )
        senha = self.validated_data['senha']
        senha2 = self.validated_data['senha2']
        if senha != senha2:
            raise serializers.ValidationError({'senha': 'As senhas precisão ser iguais!'})
        user.set_password(senha)
        user.save()

        return user

class LoginSerializer(serializers.Serializer):
    codigo = serializers.CharField(required=True)
    password = serializers.CharField(label="Senha", write_only=True, required=True, style={'input_type': 'password'})


class PontoSerializer(serializers.Serializer):
    data = serializers.DateField(format='%d/%M/%Y')

    class Meta:
        model = Ponto
        fields = ['data', 'motivo']

    def create(self, **kwargs):
        
        ponto = Ponto(
            data = self.validated_data['data'],
            motivo = self.validated_data['motivo']
        )
        self.validated_data['user'] = self.context['request'].user

        return ponto
    
class UsuarioData(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ['nome', 'setor']


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id','marca']
    
    def create(self, validated_data):
        userdt = self.context['request'].user
        marca = Marca(
            marca = unidecode(str(validated_data['marca']).upper()),
            user = userdt
        )
        
        marca.save()
        return marca

    def update(self, instance, validated_data):
        instance.marca = unidecode(str(validated_data.get('marca', instance.marca)).upper())
        instance.save()


        return instance


class MarcaListaSerializer(serializers.ModelSerializer):
    user = UsuarioData()
    criado = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    update = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    class Meta:
        model= Marca
        fields = ['id', 'marca', 'user', 'criado', 'update']


class ProdutoSerializer(serializers.ModelSerializer):
    marca = MarcaSerializer()
    class Meta:
        model = Produto
        fields = ['id','nome', 'marca']
        
    def create(self, validated_data):
        marcadt = validated_data['marca']['marca']
        userdt = self.context['request'].user
        fabri = Marca.objects.get(
            id=int(marcadt),
        )
        validated_data.pop('marca', None)
        validated_data.pop('user', None)
        name = validated_data.pop('nome')

        produto = Produto.objects.create(
            nome = unidecode(str(name).upper()),
            marca = fabri,
            user = userdt,
            **validated_data
        )
        produto.save()
        return produto
    
    def update(self, instance, validated_data):
        marca_data = validated_data.pop('marca', None)
        user = self.context['request'].user

        if marca_data:
            marca = Marca.objects.get(
                id = int(marca_data['marca']),
            )
            instance.marca = marca
        instance.nome = unidecode(str(validated_data.get('nome', instance.nome)).upper())
        instance.save()
        return instance


class ProdutoListaSerializer(serializers.ModelSerializer):
    marca = MarcaSerializer()
    user = UsuarioData()
    criado = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    update = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    class Meta:
        model= Produto
        fields = ['id', 'nome', 'marca', 'user', 'criado', 'update']


class CNPJSerializer(serializers.ModelSerializer):

    class Meta:
        model = CNPJ
        fields = ['razao_social', 'nome_fantasia', 'cnpj']

    def create(self, validated_data):
        razao = validated_data.pop('razao_social', None)
        fantasia = validated_data.pop('nome_fantasia', None)
        pj = validated_data.pop('cnpj', None)
        user = self.context['request'].user

        empresa = CNPJ.objects.create(
            razao_social=unidecode(str(razao).upper()),
            nome_fantasia=unidecode(str(fantasia).upper()),
            cnpj=unidecode(pj),
            user= user,
            **validated_data
        )
        empresa.save()
        return empresa