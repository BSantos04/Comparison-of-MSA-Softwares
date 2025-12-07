import time
import os
import subprocess
import psutil

class msa_softwares:
    def __init__(self):
        pass

    def track_usage(self, command):
        """
        Summary:
            This function tracks the execution time, peak memory usage, and peak CPU usage of the alignment run by a command line.
        
        Parameters:
            command: Input command line that will be executed.
        
        Returns:
            peak_memory: Peak memory usage (in KB) during the process run.
            exec_time: Total execution time (in seconds) of the process.
            peak_cpu_usage: Peak CPU usage (as a percentage) during the process.
        """
        # Get the starting time and baseline CPU usage
        start_time = time.time()
        baseline_cpu = psutil.cpu_percent(interval=None)

        # Start the process
        process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Initialize tracking variables
        peak_memory = 0
        peak_cpu_usage = baseline_cpu

        try:
            # While the process is still running...
            while process.poll() is None:
                # Get the process object
                proc = psutil.Process(process.pid)

                # Track the memory usage (in KB)
                mem_usage = proc.memory_info().rss / 1024
                peak_memory = max(peak_memory, mem_usage)

                # Track the CPU usage (percentage)
                cpu_usage = psutil.cpu_percent(interval=0.1)
                peak_cpu_usage = max(peak_cpu_usage, cpu_usage)

        except Exception as e:
            print(f"An error occurred while monitoring resources: {e}")

        # Ensure that the process has finished
        process.communicate()

        # Calculate the total execution time
        exec_time = time.time() - start_time

        # Return the tracked metrics
        return peak_memory, exec_time, peak_cpu_usage
    
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
        
        # Get execution time, used memory and CPU usage for that software
        memory_used, exec_time, cpu_used = self.track_usage(command)
        
        # Get the directory which the output file will be written
        pwd = os.getcwd()
        aligned_file = os.path.join(pwd, f"{filename}_mafft_aln.fasta")
        
        return aligned_file, memory_used, exec_time, cpu_used
    
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
        
        # Get execution time, used memory and CPU usage for that software
        memory_used, exec_time, cpu_used = self.track_usage(command)
                
        # Get the directory which the output file will be written
        pwd = os.getcwd()
        aligned_file = os.path.join(pwd, f"{filename}_muscle_aln.fasta")

        return aligned_file, memory_used, exec_time, cpu_used
    
    def kalign2(self, input_file):
        """
        Runs the KAlign2 alignment command on the input file and returns the aligned file along with memory and execution time.
        
        Parameters:
            input_file: Input FASTA file that contains the sequences to be aligned.
        
        Returns:
            aligned_file: Path to the file aligned by the command line.
            memory_used: Memory used during the execution of KAlign2.
            exec_time: Time taken for the execution of KAlign2.
        """
        # Get the first name of the file based on the input file name
        filename = input_file.split(".")[0]
        # Define the command line to run the software KALIGN2
        command = f"kalign -i {input_file} -o {filename}_kalign2_aln.fasta -f 0"
      
        # Get execution time, used memory and CPU usage for that software
        memory_used, exec_time, cpu_used = self.track_usage(command)
                
        # Get the directory which the output file will be written
        pwd = os.getcwd()
        aligned_file = os.path.join(pwd, f"{filename}_kalign2_aln.fasta")

        return aligned_file, memory_used, exec_time, cpu_used

    def clustalo(self, input_file):
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
                
        # Get execution time, used memory and CPU usage for that software
        memory_used, exec_time, cpu_used = self.track_usage(command)
           
        # Get the directory which the output file will be written
        pwd = os.getcwd()
        aligned_file = os.path.join(pwd, f"{filename}_clustalo_aln.fasta")

        return aligned_file, memory_used, exec_time, cpu_used
    
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
        command = f"prank -d {input_file} -o {filename}_prank_aln.fasta -f fasta"
                
        # Get execution time, used memory and CPU usage for that software
        memory_used, exec_time, cpu_used = self.track_usage(command)
           
        # Get the directory which the output file will be written
        pwd = os.getcwd()
        aligned_file = os.path.join(pwd, f"{filename}_clustalo_aln.fasta")

        return aligned_file, memory_used, exec_time, cpu_used