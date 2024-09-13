from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import logout
from .models import Usuario, Produto, Carrinho
#from .forms import ProdutoForm

# Visualização Do Inicial

def home(request):
    produtos = Produto.objects.all()
    return render(request, 'usuarios/home.html', {'produtos': produtos})

def is_admin(user):
    return user.is_staff

# Visualização Do Administrador

@user_passes_test(is_admin)
def admin_home(request):
    produtos = Produto.objects.all()
    return render(request, 'admin/admin_home.html', {'produtos': produtos})

#Visualização Do Cadastro - Usuário

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome_usuario')
        cpf = request.POST.get('cpf_usuario')
        email = request.POST.get('email_usuario')
        senha = request.POST.get('senha_usuario')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado.')
            return redirect('cadastro')

        if Usuario.objects.filter(cpf=cpf).exists():
            messages.error(request, 'CPF já cadastrado.')
            return redirect('cadastro')

        Usuario.objects.create_user(email=email, nome=nome, cpf=cpf, senha=senha)

        user = authenticate(request, username=email, password=senha)
        if user is not None:    
            auth_login(request, user)
            return redirect('home_logado')
        else:
            messages.error(request, 'Não foi possível autenticar o usuário')
            return redirect('cadastro')

    return render(request, 'usuarios/cadastro.html')

# Visualização Do Login - Usuário

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email_usuario')
        senha = request.POST.get('senha_usuario')

        user = authenticate(request, username=email, password=senha)

        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('admin_home')
            else:
                return redirect('home_logado')
        else:
            messages.error(request, 'Login inválido')
            return render(request, 'usuarios/login_usuario.html')

    return render(request, 'usuarios/login_usuario.html')

# Visualização Do Sistema de Logout Implementado

def logout_teste(request):
    logout(request)
    return redirect('home')

# Visualização Do Carrinho do Cliente

@login_required
def carrinho(request):
    carrinho_items = Carrinho.objects.filter(usuario=request.user)
    subtotal = sum(item.produto.preco * item.quantidade for item in carrinho_items)
    return render(request, 'usuarios/carrinho.html', {'carrinho_items': carrinho_items, 'subtotal': subtotal})

# Visualização Do Home só que Logado, após Cadastro ou Login

@login_required
def home_logado(request):
    usuario = request.user
    produtos = Produto.objects.all()
    
    categoria = request.GET.get('categoria')
    if categoria:
        produtos = produtos.filter(categoria=categoria)
    
    context = {
        'usuario': usuario,
        'produtos': produtos,
    }
    return render(request, 'usuarios/home_logado.html', context)

# Visualização Do CRUD implementado para o usuário, modificação de dados e exclusão de conta do usuário logado

@login_required
def crud_usuario(request):
    usuario = request.user

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')

        usuario.nome = nome
        usuario.email = email
        usuario.cpf = cpf

        if senha:
            usuario.set_password(senha)
            update_session_auth_hash(request, usuario)

        usuario.save()
        messages.success(request, 'Dados atualizados com sucesso!')
        return redirect('crud_usuario')

    return render(request, 'usuarios/crud_usuario.html', {'usuario': usuario})

# Visualização Do Sistema para Excluir a Conta dentro do CRUD do Usuário

@login_required
def excluir_conta(request):
    usuario = request.user

    if request.method == 'POST':
        # Logout antes de excluir o usuário
        logout(request)
        usuario.delete()
        messages.success(request, 'Conta excluída com sucesso!')
        return redirect('home')

    return render(request, 'usuarios/excluir_conta.html', {'usuario': usuario})

# Visualização Do Sistema de Remover Produtos do Carrinho

@login_required
def remover_do_carrinho(request, carrinho_id):
    carrinho_item = get_object_or_404(Carrinho, id=carrinho_id, usuario=request.user)
    carrinho_item.delete()
    messages.success(request, 'Produto removido do carrinho!')
    return redirect('carrinho')

# Visualização Do Sistema implementado para atualizar a Quantidade de Produtos no Carrinho do Usuário Logado
# Atualizando também o sistema de cálculo

@login_required
def atualizar_quantidade(request, carrinho_id):
    carrinho_item = get_object_or_404(Carrinho, id=carrinho_id, usuario=request.user)
    nova_quantidade = int(request.POST.get('quantidade'))
    if nova_quantidade > 0:
        carrinho_item.quantidade = nova_quantidade
        carrinho_item.save()
        messages.success(request, 'Quantidade atualizada!')
    else:
        carrinho_item.delete()
        messages.success(request, 'Produto removido do carrinho!')
    return redirect('carrinho')

# Visualização Do Sistema usado para Adicionar Produtos ao Carrinho do Usuário logado

@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho_item, created = Carrinho.objects.get_or_create(usuario=request.user, produto=produto)
    if not created:
        carrinho_item.quantidade += 1
    carrinho_item.save()
    messages.success(request, 'Produto adicionado ao carrinho!')
    return redirect('home_logado')

# Visualização Do Sistema usado para Efetuar a Compra e Descontar do Estoque

@login_required
def finalizar_compra(request):
    usuario = request.user
    carrinho_items = Carrinho.objects.filter(usuario=usuario)

    if not carrinho_items.exists():
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('carrinho')

    for item in carrinho_items:
        produto = item.produto
        if produto.quantidade < item.quantidade:
            messages.error(request, f'Estoque insuficiente para {produto.nome}.')
            return redirect('carrinho')
        produto.quantidade -= item.quantidade
        produto.save()
    
    carrinho_items.delete()
    messages.success(request, 'Compra finalizada com sucesso!')
    return redirect('home_logado')

# Visualização Do Sistema criado para Adicionar/Criar Produtos ao Estoque da Loja

def adicionar_produto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        preco = request.POST.get('preco')
        descricao = request.POST.get('descricao')
        imagem = request.FILES.get('imagem')
        quantidade = request.POST.get('quantidade')

        if not nome or not preco or not descricao or not quantidade:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, 'admin/adicionar_produto.html')

        try:
            preco = float(preco)
        except ValueError:
            messages.error(request, 'O preço deve ser um número válido.')
            return render(request, 'admin/adicionar_produto.html')

        produto = Produto(nome=nome, preco=preco, descricao=descricao, imagem=imagem, quantidade=quantidade)
        produto.save()

        messages.success(request, 'Produto adicionado com sucesso!')
        return redirect('admin_home')

    return render(request, 'admin/adicionar_produto.html')

# Visualização Do Sistema criado para Editar as informações dos Produtos criados

def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        nome = request.POST.get('nome')
        preco = request.POST.get('preco')
        descricao = request.POST.get('descricao')
        imagem = request.FILES.get('imagem')
        quantidade = request.POST.get('quantidade')

        produto.nome = nome
        produto.preco = preco
        produto.descricao = descricao
        produto.quantidade = quantidade
        if imagem:
            produto.imagem = imagem
        
        produto.save()
        messages.success(request, 'Produto atualizado com sucesso!')
        return redirect('admin_home')
    
    return render(request, 'admin/editar_produto.html', {'produto': produto})

# Visualização Do Sistema criado para Excluir Produtos existentes no estoque

def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.delete()
    messages.success(request, 'Produto excluído com sucesso!')
    return redirect('admin_home')



