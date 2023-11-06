import sqlite3
import random
from datetime import datetime
import calendar

# Conecta-se ao banco de dados SQLite
conn = sqlite3.connect(r'C:\Users\jesse\OneDrive\Documentos\Projetos_Python\medicaohidrica\db.sqlite3')
cursor = conn.cursor()

# Define o ID do usuário
usuario_id = 6

# Loop para gerar e inserir dados de janeiro a dezembro
for mes in range(1, 13):
    # Obter o último dia do mês
    ultimo_dia = calendar.monthrange(2023, mes)[1]
    
    for dia in range(1, ultimo_dia + 1):
      
        dt = datetime(2023, mes, dia).strftime('%Y-%m-%d')
        m3 = round(random.uniform(1, 100), 2)
        total = round(m3 * random.uniform(1, 4), 2)  # Quanto maior m3, maior total
        
        if total > 400:
            total = 400  # Limita o total a 400

        cursor.execute("INSERT INTO divulgar_medicao (dt, m3, total, usuario_id) VALUES (?, ?, ?, ?)",
                       (dt, m3, total, usuario_id))

conn.commit()
conn.close()