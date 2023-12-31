from django.db import models
from django.contrib.auth.models import User # Importe o modelo de usuário
from datetime import datetime

# Create your models here.   
    
class Medicao(models.Model):
    
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    dt      = models.DateField(default=datetime.now)
    m3      = models.FloatField()
    total   = models.FloatField()

