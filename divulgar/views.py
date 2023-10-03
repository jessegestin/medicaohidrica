from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Medicao
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@login_required
def novo_registro(request):
    if request.method == "GET":
        return render(request, 'novo_registro.html')
    elif request.method == "POST":
        dt  = request.POST.get('dt')
        m3    = request.POST.get('m3')
        total = request.POST.get('total')
        
        #TODO: Validar dados

        medicao = Medicao(
            usuario=request.user,
            dt=dt,
            m3=m3,
            total=total,
         )

        medicao.save()
        
        medicao.save()
        
        messages.add_message(request, constants.SUCCESS, 'Nova medição cadastrada')
        
        return render(request, 'novo_registro.html')
    
@login_required
def seus_registros(request):
    if request.method == "GET":
        medicao = Medicao.objects.filter(usuario=request.user)
        return render(request, 'seus_registros.html', {'medicao': medicao})
    
@login_required
def remover_registro(request, id):
    medicao = Medicao.objects.get(id=id)
    
    if not medicao.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Essa medição pertence a outro usuário!')
        return redirect('/divulgar/seus_registros')

    medicao.delete()
    messages.add_message(request, constants.SUCCESS, 'Removido com sucesso.')
    return redirect('/divulgar/seus_registros')

@login_required
def ver_registro(request, id):
    if request.method == "GET":
        medicao = Medicao.objects.get(id = id)
        return render(request, 'ver_registro.html', {'medicao': medicao})
    
@login_required    
def dashboard(request):
    if request.method == "GET":
        return render(request, 'dashboard.html')