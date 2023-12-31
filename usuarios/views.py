from django.shortcuts import render
from django.http import HttpResponse
from  django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
# Create your views here.

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_registro')
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST" :
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        print(nome, email, senha, confirmar_senha)
        
        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return render(request, 'cadastro.html')
        elif senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Digite duas senhas iguais')
            return render(request, 'cadastro.html')
        
        try:
            user = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )
            # Mensagem sucesso
            messages.add_message(request, constants.SUCCESS, 'Usuário criado com sucesso!')
            return render(request, 'login.html')
        except:
            # Mensagem erro
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return render(request, 'cadastro.html')
        
        # return HttpResponse(f'{nome}, {email}, {senha}, {confirmar_senha}')
        
def logar(request):
    if request.user.is_authenticated:
        return redirect('/divulgar/seus_registros')
    if request.method == "GET":
       return render(request, 'login.html')
    elif request.method == "POST":
       nome = request.POST.get('nome')
       senha = request.POST.get('senha')
       user = authenticate(username=nome,
                           password=senha)
       
       if user is not None:
         # Vou Logar
         login(request, user)
         return redirect('/divulgar/seus_registros')
       else: 
         messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
         return render(request, 'login.html')
       
       # return HttpResponse(f'{nome} {senha}')
       
def sair(request):
    logout(request)
    return redirect('/auth/login')