import subprocess
import psutil
import sys

def mede_CPU_utilizado(comando):
    processo = subprocess.Popen(comando, shell=True)
    utilização_base=psutil.cpu_percent()
    em_utilização = 0
    em_utilização_t = 0

    try:
        while processo.poll() is None:
        em_utilização = psutil.cpu_percent(interval=1)
        em_utilização = max(em_utilização, em_utilização_t)
        em_utilização_t = em_utilização

    except Exception as erro_utilização:
        print(f"Erro ao determinar a CPU utilizada: {erro_utilização}")
    em_utilização = em_utilização_t - utilização_base

    return  em_utilização
