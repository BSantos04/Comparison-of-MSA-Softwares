import time
import subprocess
import psutil
import os

class msa_softwares:
    def __init__(self):
        pass
    
    def get_memory_and_time(self, command):
        """
        Summary:
            This function gets the execution time and used memory of a process run by a command line.
            
        Parameters:
            command: Input command line that will be parsed.
            
        Returns:
            used_memory: Memory that was used during the process run by the command line.
            exec_time: Time of execution of the process run by the command line.

        """
        # Get starting time of the process
        start_time = time.time()
        
        # Start the process 
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Monitor the memory usage 
        peak_memory = 0
        try:
            # While the process is still running...
            while process.poll() is None:
                # Get the process object
                proc = psutil.Process(process.pid)
                # Track the memory that is being used in KB
                mem_usage = proc.memory_info().rss / 1024
                # Get the peak memory ever registered during the process
                peak_memory = max(peak_memory, mem_usage)
                # In order to avoid high CPU while polling, we gve a short period of rest
                time.sleep(0.1)
        except Exception as e:
            print(f"An error has occurred: {e}")
        
        # Ensure that the process has finished and get the output
        process.communicate()
        # Get the execution time (difference between finish time and start time)
        exec_time = time.time() - start_time
        # Define used memory as peak memory registered
        memory_used = peak_memory

        return memory_used, exec_time
    
    def mafft(self, input_file):
        """
        Runs the MAFFT alignment command on the input file and returns the aligned file along with memory and execution time.
        
        Parameters:
            input_file: Input FASTA file that contains the sequences to be aligned.
        
        Returns:
            aligned_file: Path to the file aligned by the command line.
            memory_used: Memory used during the execution of MAFFT.
            exec_time: Time taken for the execution of MAFFT.
        """
        # Get the first name of the file based on the input file name
        filename = input_file.split(".")[0]
        # Define the command line to run the software MAFFT
        command = f"mafft {input_file} > {filename}_mafft_aln.fasta"
        
        # Get execution time and used memory for that software
        memory_used, exec_time = self.get_memory_and_time(command)
        
        # Get the directory which the output file will be written
        pwd = os.getcwd()
        aligned_file = os.path.join(pwd, f"{filename}_mafft_aln.fasta")
        
        return aligned_file, memory_used, exec_time
    
    def muscle(self, input_file):
        """
        Runs the MUSCLE alignment command on the input file and returns the aligned file along with memory and execution time.
        
        Parameters:
            input_file: Input FASTA file that contains the sequences to be aligned.
        
        Returns:
            aligned_file: Path to the file aligned by the command line.
            memory_used: Memory used during the execution of MUSCLE
            exec_time: Time taken for the execution of MUSCLE.
        """
        # Get the first name of the file based on the input file name
        filename = input_file.split(".")[0]
        # Define the command line to run the software MUSCLE
        command = f"muscle -align {input_file} -output {filename}_muscle_aln.fasta"
                
        # Get execution time and used memory for that software
        memory_used, exec_time = self.get_memory_and_time(command)
                
        # Get the directory which the output file will be written
        pwd = os.getcwd()
        aligned_file = os.path.join(pwd, f"{filename}_muscle_aln.fasta")
        
        return aligned_file, memory_used, exec_time
    
    def tcoffee(self, input_file):
        """
        Runs the T-Coffee alignment command on the input file and returns the aligned file along with memory and execution time.
        
        Parameters:
            input_file: Input FASTA file that contains the sequences to be aligned.
        
        Returns:
            aligned_file: Path to the file aligned by the command line.
            memory_used: Memory used during the execution of T-Coffee.
            exec_time: Time taken for the execution of T-Coffee.
        """
        # Get the first name of the file based on the input file name
        filename = input_file.split(".")[0]
        # Define the command line to run the software T-Coffee
        command = f"t_coffee -in {input_file} -output fasta_aln -outfile {filename}_tcoffee_aln.fasta"
                
        # Get execution time and used memory for that software
        memory_used, exec_time = self.get_memory_and_time(command)
                
        # Get the directory which the output file will be written
        pwd = os.getcwd()
        aligned_file = os.path.join(pwd, f"{filename}_tcoffee_aln.fasta")
        
        return aligned_file, memory_used, exec_time
    
    def clustalomega(self, input_file):
        """
        Runs the ClustalOmega alignment command on the input file and returns the aligned file along with memory and execution time.
        
        Parameters:
            input_file: Input FASTA file that contains the sequences to be aligned.
        
        Returns:
            aligned_file: Path to the file aligned by the command line.
            memory_used: Memory used during the execution of ClustalOmega.
            exec_time: Time taken for the execution of ClustalOmega.
        """
        # Get the first name of the file based on the input file name
        filename = input_file.split(".")[0]
        # Define the command line to run the software ClustalOmega
        command = f"clustalo -i {input_file} -o {filename}_clustalo_aln.fasta --outfmt fasta"
                
        # Get execution time and used memory for that software
        memory_used, exec_time = self.get_memory_and_time(command)
                
        # Get the directory which the output file will be written
        pwd = os.getcwd()
        aligned_file = os.path.join(pwd, f"{filename}_clustalo_aln.fasta")
        
        return aligned_file, memory_used, exec_time
    
    def prank(self, input_file):
        """
        Runs the PRANK alignment command on the input file and returns the aligned file along with memory and execution time.
        
        Parameters:
            input_file: Input FASTA file that contains the sequences to be aligned.
        
        Returns:
            aligned_file: Path to the file aligned by the command line.
            memory_used: Memory used during the execution of PRANK.
            exec_time: Time taken for the execution of PRANK.
        """
        # Get the first name of the file based on the input file name
        filename = input_file.split(".")[0]
        # Define the command line to run the software PRANK
        command = f"prank -d={input_file} -o={filename}_prank_aln"
                
        # Get execution time and used memory for that software
        memory_used, exec_time = self.get_memory_and_time(command)
                
        # Get the directory which the output file will be written
        pwd = os.getcwd()
        aligned_file = os.path.join(pwd, f"{filename}_prank_aln.best.fas")
        
        return aligned_file, memory_used, exec_time
 