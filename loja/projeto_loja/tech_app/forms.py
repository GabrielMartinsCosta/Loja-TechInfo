# Quaisquer duvidas aqui eu explico
# Foi uma tentativa de usar o forms para fazer alguns sistemas do views.py
# Sem sucesso, acabei deixando comentado para não ser utilizado
# Bom ponto para rever depois.
# 
# from django import forms
#from .models import Produto

#class ProdutoForm(forms.ModelForm):
    #class Meta:
       # model = Produto
        #fields = ['nome', 'preco', 'descricao', 'imagem', 'quantidade']

    #def clean_preco(self):
       # preco = self.cleaned_data['preco']
       # try:
       #     float(preco)  # Verifica se o preço pode ser convertido para float
      #  except ValueError:
       #     raise forms.ValidationError("O preço deve ser um número válido.")
       # return preco
