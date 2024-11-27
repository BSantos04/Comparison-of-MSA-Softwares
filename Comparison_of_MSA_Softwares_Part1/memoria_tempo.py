import time
import os
import psutil


def get_memory_and_time(command):
    """
    Summary: 
        This function gets the execution time and used memory of a process run by a command line.
        
    Parameters:
        command: Input command line that will be parsed.
        
    Returns:
        used_memory: Memory that was used during the process run by the command line.
        exec_time: Time of execution of the process run by the command line.

    """
    start_time = time.time()
    process = os.system(command)
    start_memory = psutil.virtual_memory().used / (1024)
    total_memory = start_memory
    try:
        while process.poll():
            interim_total_memory = psutil.virtual_memory().used / (1024)
            total_memory = max(interim_total_memory)
    except Exception as e:
        print(f"An error has occured:\n{e}")
    used_memory = total_memory - start_memory
    exec_time = time.time() - start_time

    return used_memory, exec_time
