from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Sistema de Gerenciador de Usuários que são criados pelo front
# Para registrar super usuário = Usar o sistema do próprio shell do django
# Visto que o Usuário é costumizado

class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, nome, cpf, senha=None, id_cliente=None, **extra_fields):
        if not email:
            raise ValueError('O email precisa ser fornecido')
        email = self.normalize_email(email)
        usuario = self.model(email=email, nome=nome, cpf=cpf, id_cliente=id_cliente, **extra_fields)
        usuario.set_password(senha)
        usuario.save(using=self._db)
        return usuario
    
    def create_superuser(self, email, nome, cpf, senha=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, nome, cpf, senha=senha, **extra_fields)

# Sistema de Criação do Usuário Customizado no Banco de Dados
# Tabelas funcionais e validadas por sistema de autenticação no views.py
# Neste projeto utilizei o MySQL

class Usuario(AbstractBaseUser):

    id_cliente = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cpf'] #'cpf'

    objects = UsuarioManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
    
# Sistema de Criação dos Produtos utilizados no projeto
# Atualizando também de forma funcional o Database do SQL

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='media/', null=True, blank=True)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return self.nome
    
# Para finalizar, Criação do Carrinho que o usuário vai manipular de acordo com suas necessidades
# Atualizado constante com os produtos, guarda de forma funcional na tabela

class Carrinho(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome} ({self.usuario.email})"
    

