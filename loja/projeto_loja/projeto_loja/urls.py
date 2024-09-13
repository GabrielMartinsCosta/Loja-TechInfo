"""
URL configuration for projeto_loja project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tech_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', views.admin_home, name='admin_home'),
    path('admin/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('editar_produto/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('admin/excluir_produto/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),
    path('',views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login_usuario/', views.login_view, name='login'),
    path('home_logado/', views.home_logado, name='home_logado'),
    path('crud_usuario/', views.crud_usuario, name='crud_usuario'),
    path('excluir_conta/', views.excluir_conta, name='excluir_conta'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('adicionar_ao_carrinho/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover_do_carrinho/<int:carrinho_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('finalizar_compra/', views.finalizar_compra, name='finalizar_compra'),
    path('atualizar_quantidade/<int:carrinho_id>/', views.atualizar_quantidade, name='atualizar_quantidade'),
    path('logout/', views.logout_teste, name='logout_teste'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

   #path('usuarios/', views.usuarios, name='listagem'),