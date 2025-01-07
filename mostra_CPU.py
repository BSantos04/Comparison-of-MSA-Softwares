import psutil
import time
import sys

def mede_CPU_utilizado():
    utilização_base=psutil.cpu_percent()    

    tempo_0 = 1
    tempo_c = 20
    intervalo = 1
    em_utilização_t = 0

    while tempo_0 > tempo_c:
        em_utilização = psutil.cpu_percent()
        em_utilização = max(em_utilização, em_utilização_t)
        em_utilização_t = em_utilização

        time.sleep(intervalo)
        tempo_0 += 1

    em_utilização = em_utilização_t - utilização_base
    
    print(f"A CPU utilizada no processo foi {em_utilização}%")
    
if __name__ == "__main__":
    if len(sys.argv)!=1:
        print("Usage: python3 {path/to/script.py}")
    else:
        mede_CPU_utilizado()