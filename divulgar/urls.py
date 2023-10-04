from django.urls import path
from . import views

urlpatterns = [
    path('novo_registro/', views.novo_registro, name="novo_registro"),
    path('seus_registros/', views.seus_registros, name="seus_registros"),
    path('remover_registro/<int:id>', views.remover_registro, name="remover_registro"),
    path('ver_registro/<int:id>', views.ver_registro, name="ver_registro"),
    path('dashboard/', views.dashboard, name="dashboard")
]