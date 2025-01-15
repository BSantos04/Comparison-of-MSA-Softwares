import subprocess
import psutil
import sys

def mede_CPU_utilizado(comando):
    # input comando corrido em shell
    processo = subprocess.Popen(comando, shell=True)
    # verifica a CPU a cer utilizada antes do começo do processo
    utilização_base=psutil.cpu_percent()
    # criação das variaveis
    em_utilização = 0
    em_utilização_t = 0
    # enquanto o comado incerido tiver a correr vai verificar a cpu a ser utiliza e sendo atribuido o maior a em_utilização_t,
    # entre em_utilização e em_utilização_t se e a vairiavel em_utilização_t vai ficar com o maior valor e quando o processo o ciclo para
    try:
        while processo.poll() is None:
            em_utilização = psutil.cpu_percent()
            em_utilização = max(em_utilização, em_utilização_t)
            em_utilização_t = em_utilização
    # caso de erro imprime a função Erro ao determinar a CPU utilizada: {erro_utilização}
    except Exception as erro_utilização:
        print(f"Erro ao determinar a CPU utilizada: {erro_utilização}")
    # vai calcular a diferença entre a utilização da CPU inicial e o maior valor da utilização que vai cer a utilização ao longo do processo
    em_utilização = em_utilização_t - utilização_base

    # vai retornar o valor
    return  em_utilização
