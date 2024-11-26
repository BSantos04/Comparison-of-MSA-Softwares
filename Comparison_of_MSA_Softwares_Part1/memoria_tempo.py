import time
import os
import psutil


def memoria_tempo(comando):
    tempo_inicio = time.time()
    processo = os.system(comando)
    memoria_inicial = psutil.virtual_memory().used / (1024)
    memoria_total = memoria_inicial
    try:
        while processo.poll():
            memoria_total_c = psutil.virtual_memory().used / (1024)
            memoria_total = max(memoria_total_c)
    except Exception as erro_memoria:
        print(f"Erro ao determinar a memoria {erro_memoria}")
    memoria_utilizada = memoria_total-memoria_inicial
    tempo_utilizado = time.time()-tempo_inicio

    return memoria_utilizada, tempo_utilizado