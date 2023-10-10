from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Medicao
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import json
from django.views.decorators.http import require_GET
import babel
from babel import numbers
# Importe o módulo decimal para lidar com números decimais
import decimal

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
        medicao = Medicao.objects.filter(usuario=request.user).order_by('dt')
        
        # Configurar o ambiente para o formato de moeda brasileira
        brazilian_locale = babel.Locale('pt_BR')
        
        # Formatar os valores como moeda antes de passá-los para o modelo
        for m in medicao:            
            m.m3_formatado = "{:.2f}".format(decimal.Decimal(m.m3)).replace('.', ',')
            m.total_formatado = numbers.format_currency(m.total, 'BRL', locale=brazilian_locale)
        
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
    
@require_GET
def dashboard(request, selected_month=None):
    if selected_month is None:
        # Se selected_month for None, defina-o como o mês atual (por exemplo, "01" para janeiro)
        selected_month = datetime.now().strftime('%m')
    else:
        # Certifique-se de que selected_month é um valor válido no formato "01", "02", etc.
        if selected_month:
            try:
                selected_month = int(selected_month)
                if not (1 <= selected_month <= 12):
                    selected_month = datetime.now().strftime('%m')
                else:
                    selected_month = f"{selected_month:02d}"
            except ValueError:
                selected_month = datetime.now().strftime('%m')
        else:
            selected_month = datetime.now().strftime('%m')

    # Filtre os dados com base no mês selecionado (ou no mês atual)
    dados_medicao = Medicao.objects.filter(
        usuario=request.user,  # Filtrar pelo usuário logado
        dt__month=selected_month).order_by('dt')

    datas = [int(obj.dt.strftime('%d')) for obj in dados_medicao]
    valores = [float(obj.m3) for obj in dados_medicao]  # Usar float para valores em ponto flutuante

    context = {
        'datas': json.dumps(datas, ensure_ascii=False),
        'valores': json.dumps(valores, ensure_ascii=False),
    }

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(context)  # Se a solicitação for AJAX, retorne uma resposta JSON
    else:
        return render(request, 'dashboard.html', context)