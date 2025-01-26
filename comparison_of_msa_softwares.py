import time
import os
import subprocess
import sys
import psutil
import shutil
from Bio import AlignIO
import matplotlib.pyplot as plt
import pandas as pd

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
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
                
        # Get execution time, used memory and CPU usage for that software
        memory_used, exec_time, cpu_used = self.track_usage(command)
                
        # Get the directory which the output file will be written
        pwd = os.getcwd()
        aligned_file = os.path.join(pwd, f"{filename}_tcoffee_aln.fasta")
        
        return aligned_file, memory_used, exec_time, cpu_used
    
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
        command = f"prank -d={input_file} -o={filename}_prank_aln"
                
        # Get execution time, used memory and CPU usage for that software
        memory_used, exec_time, cpu_used = self.track_usage(command)
                
        # Get the directory which the output file will be written
        pwd = os.getcwd()
        aligned_file = os.path.join(pwd, f"{filename}_prank_aln.best.fas")
        
        return aligned_file, memory_used, exec_time, cpu_used
    
class SPScore:
    def __init__(self, matrix_file):
        """
        Initializes the scoring_matrix object and loads the scoring matrix.
        
        Parameters:
            matrix_file: Path to the scoring matrix file in BLAST format.
        """
        self.scoring_matrix = self.load_matrix(matrix_file)

    def read_scoring_matrix(self, file, parse_matrix=lambda x: x):
        """
        Reads a BLAST format matrix and yields key-value pairs for the matrix.
        
        Parameters:
            file: Input file object containing the BLAST format matrix.
            parse_matrix: Function to transform the matrix values. Default returns values unchanged.
        
        Yields:
            ((row_id, col_id), parse_matrix(matrix_cell)): Tuple matrix containing each possible pair of nucleotides/proteins and their respective scores.
        """
        # Reading and splitting all the lines/rows of the matrix
        rows = (line.rstrip().split() for line in file)
        
        # Extracting the headers/column identifiers of the matrix
        header = next(rows)
        
        # Processing rows
        # Ensuring that every character is in upper case
        for row in rows:
            row_id = row[0].upper()
            
            # Iterating through matrix cells, pairing each column identifier with its corresponding matrix value
            for col_id, matrix_cell in zip(header, row[1:]):
                yield ((row_id, col_id), parse_matrix(matrix_cell))

    def load_matrix(self, matrix_file):
        """
        Opens the matrix file and processes it into a dictionary object.
        
        Parameters:
            matrix_file: Path to the scoring matrix file.
        
        Returns:
            {key: int(value) for key, value in matrix.items()}: Dictionary representing the scoring matrix.
        """
        # Open matrix file
        with open(matrix_file) as f:
            # Parse the file and convert it into a dictionary
            matrix = dict(self.read_scoring_matrix(f))
            # Convert all values to integers
            return {key: int(value) for key, value in matrix.items()}

    def affine_gap_penalty(self, gap_len, gapO=-6, gap_ext=-1):
        """
        Calculates the affine gap penalty score for a given gap length.
        
        Parameters:
            gap_len: Length of the gap in an aligned sequence.
            gapO: Gap opening penalty (default: -6).
            gap_ext: Gap extension penalty per unit length (default: -1).
        
        Returns:
            gapO + gap_len * gap_ext: The affine gap penalty score formula.
        """
        return gapO + gap_len * gap_ext

    def pairwise_score(self, seq1, seq2):
        """
        Calculates the pairwise score of two aligned sequences using the scoring matrix and gap penalties.
        
        Parameters:
            seq1: First sequence of the pair.
            seq2: Second sequence of the pair.
        
        Returns:
            score: The total pairwise score for the given sequences.
        """
        # Define vraiables for the total score and number of gaps for both sequences with default values
        score = 0
        gap1, gap2 = 0, 0

        # Loop through pairs of characters from the two sequences
        # For each match/mismatch, it will give the respective score for each pair of nucleotides/proteins
        # If both match caharcters are gaps the code will skip and count it as zero
        for a, b in zip(seq1, seq2):
            if a == "-" and b == "-":
                continue
            if a == "-" or b == "-":
                if a == "-":
                    gap1 += 1
                    if gap2 > 0:
                        score += self.affine_gap_penalty(gap2)
                        gap2 = 0
                if b == "-":
                    gap2 += 1
                    if gap1 > 0:
                        score += self.affine_gap_penalty(gap1)
                        gap1 = 0
            else:
                if gap1 > 0:
                    score += self.affine_gap_penalty(gap1)
                    gap1 = 0
                if gap2 > 0:
                    score += self.affine_gap_penalty(gap2)
                    gap2 = 0
                score += self.scoring_matrix.get((a, b), 0)

        return score

    def sp_score(self, aligned_file):
        """
        Summary:
            Using all the helper functions previously created, we calculate the SP-Score of an aligned file based on the defined
            scoring matrix and the defined gap penalties.
        
        Parameters:
            aligned_file: FASTA file containing the aligned sequences.
        
        Returns:
            sp_score: SP-Score calculated for the input aligned file.

        """
        # Parsing the aligned FASTA file into an AlignIO object
        alignment = AlignIO.read(aligned_file, "fasta")
        
        # Determine the number of sequences on the aligned file and creating an object to handle the SP-Score value
        num_seqs = len(alignment)
        sp_score = 0

        # Calculates the pairwise score for every pair of sequences of the file
        for i in range(num_seqs):
            for j in range(i + 1, num_seqs):
                # We are just ensuring that every character of the sequences are upper case
                seq1 = str(alignment[i].seq).upper()
                seq2 = str(alignment[j].seq).upper()
                # Add all the obtained pairwise score values to the sp_score object
                sp_score += self.pairwise_score(seq1, seq2)

        return sp_score
    
def overall_score(ref_info, sp_dict, mem_dict, time_dict, cpu_dict):
    """
    Summary:
        This function calculates the overall score for one alignment based on the SP-Score, memory, execution time and cpu usage values obtained.
    
    Parameters:
        ref_info: Information of the aligned that is going to be analyzed and we are calculating the overall score.
        sp_dict: A dictionary containing the values of all SP-Scores of all alignments.
        mem_dict: A dictionary containing the values of all used memories of all alignments.
        time_dict: A dictionary containing the values of all execution times of all alignments.
        cpu_dict: A dictionary containing the values of all CPU usage of all alignments.
    
    Returns:
        score: Overall score for the reference alignment.

    """
    # Get the aligned file path, used memory and execution time of the reference alignment
    aln, memory, exectime, cpu = ref_info
    
    # Create list for every values of SP-Scores, used memories, execution times and cpu usage
    sp_scores = list(sp_dict.values())
    mems = list(mem_dict.values())
    times = list(time_dict.values())
    cpus = list(cpu_dict.values())
    
    # Get the SP-Score for the reference alignment
    aln_spscore = spscore.sp_score(aln)
    
    # Since the SP-Score values can be negative (like, very negative), we are gonna need to transform them first
    min_spscore = min(sp_scores)
    aln_spscore += min_spscore
    for i in range(len(sp_scores)):
        sp_scores[i] += min_spscore
    
    # Normalize the SP-Score value in order to correspond to our overall score 
    normalized_spscore = (aln_spscore*5)/max(sp_scores)
    
    # Noramlize the memory value in order to correspond to our overall score
    normalized_memory = (1/memory)/(1/min(mems))
    
    # Normalize the execution time value in order to corresponf to our overall score
    normalized_time = ((1/exectime))/(1/min(times))
    
    # Normalize the cpu value in order to corresponf to our overall score
    normalized_cpu = ((1/cpu))/(1/min(cpus))
    
    # Calculate the score for the reference alignment
    score = normalized_spscore + normalized_memory + normalized_time + normalized_cpu
    
    return score

def create_bar_plot(info_dict, ylabel, title):
    """
    Summary: 
        Creates a bar plot with the values displayed on top of each bar.

    Parameters:
        info_dict: Dictionary with software names as keys and parameter values as values.
        ylabel: Label for the y-axis of the bar plot.
        title: Title of the bar plot.

    Returns:
        plot_file_path: The absolute path to the saved bar plot image file.
    """
    # Extract keys and values based on the given dictionary
    labels = list(info_dict.keys())
    values = list(info_dict.values())
    
    # Create the bar plot
    fig, ax = plt.subplots()
    bars = ax.bar(labels, values, color="blue", width=0.5)
    
    # Add labels and a title
    ax.set_xlabel("MSA Softwares")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    # Display the value on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # x position
            height,  # y position
            f'{height:.3f}',  # Text to display with two decimal points
            ha='center',  # Horizontal alignment
            va='bottom',  # Vertical alignment
            fontsize=10,  # Font size
            color="black"  # Text color
        )
    
    # Saving the plot into a file
    filename = "_".join(title.split())
    plot_file_path = os.path.abspath(f"{filename}.png")
    plt.tight_layout()  # Adjust layout to prevent overlapping
    plt.savefig(plot_file_path)
    
    # Free up memory by closing the plot
    plt.close()
    
    return plot_file_path  
    
def create_table(sp_scores, memories, times, cpus, o_scores):
    """
    Summary: 
        Creates a table with every MSA software and their respective scores for every parameter.

    Parameters:
        sp_scores: Dictionary containing the SP-Scores of every MSA software.
        memories: Dictionary containing the RAM usage of every MSA software.
        times: Dictionary containing the execution time of every MSA software.
        cpus: Dictionary containing the CPU usage of every MSA software.
        o_scores: Dictionary containing the overall scores of every MSA software.

    Returns:
        table: The table object without the indexes of each list parameter (MSA softwares)

    """
    # Create lists containing the values of each parameter dictionary
    sp_list = list(sp_scores.values())
    memories_list = list(memories.values())
    times_list = list(times.values())
    cpu_list = list(cpus.values())
    o_list = list(o_scores.values())
    
    # Create a dictionary containing the data that will be used to create the table
    d = {
         "MSA Software": ["MAFFT", "MUSCLE", "T-Coffee", "ClustalOmega", "PRANK"],
         "SP-Score": sp_list,
         "RAM Usage": memories_list,
         "Time": times_list,
         "CPU Usage": cpu_list, 
         "Overall Score": o_list}
    
    # Convert the data into a dataframe
    df = pd.DataFrame(data=d)
    
    # Create the table object removing the indexes
    table = df.to_string(index=False) + "\n"
    
    return table
    
# Just ensuring the code is only executed when the script is run as a standalone program.
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 {path/to/sequences/file.fasta} {path/to/scoring/matrix/file}")
    else:
        # Creating instances for the classes using the needed parameters
        spscore = SPScore(sys.argv[2])
        msa = msa_softwares()
        
        # Run all the MSA softwares
        mafft_info = msa.mafft(sys.argv[1])
        muscle_info = msa.muscle(sys.argv[1])
        tcoffee_info = msa.tcoffee(sys.argv[1])
        clustalo_info = msa.clustalomega(sys.argv[1])
        prank_info = msa.prank(sys.argv[1])
        
        # Get all returned objects from each alignment (aligned file, used memory, execution time and cpu usage)
        mafft_aln, mafft_memory, mafft_time, mafft_cpu = mafft_info
        muscle_aln, muscle_memory, muscle_time, muscle_cpu = muscle_info
        tcoffee_aln, tcoffee_memory, tcoffee_time, tcoffee_cpu = tcoffee_info
        clustalo_aln, clustalo_memory, clustalo_time, clustalo_cpu = clustalo_info
        prank_aln, prank_memory, prank_time, prank_cpu = prank_info
        
        
        # Get a dictionary of each parameter value of every MSA software
        msa_files = {"MAFFT": mafft_aln,
                    "MUSCLE": muscle_aln,
                    "T-Coffee": tcoffee_aln,
                    "ClustalOmega": clustalo_aln,
                    "PRANK": prank_aln}
        
        memories = {"MAFFT": mafft_memory,
                    "MUSCLE": muscle_memory,
                    "T-Coffee": tcoffee_memory,
                    "ClustalOmega": clustalo_memory,
                    "PRANK": prank_memory}
        
        times = {"MAFFT": mafft_time,
                 "MUSCLE": muscle_time,
                 "T-Coffee": tcoffee_time,
                 "ClustalOmega": clustalo_time,
                 "PRANK": prank_time}
        
        cpus = {"MAFFT": mafft_cpu,
                 "MUSCLE": muscle_cpu,
                 "T-Coffee": tcoffee_cpu,
                 "ClustalOmega": clustalo_cpu,
                 "PRANK": prank_cpu}
        
        sp_scores = {"MAFFT": spscore.sp_score(mafft_aln),
                    "MUSCLE": spscore.sp_score(muscle_aln),
                    "T-Coffee": spscore.sp_score(tcoffee_aln),
                    "ClustalOmega": spscore.sp_score(clustalo_aln), 
                    "PRANK": spscore.sp_score(prank_aln)}
        
        o_scores = {"MAFFT": overall_score(mafft_info, sp_scores, memories, times, cpus),
                    "MUSCLE": overall_score(muscle_info, sp_scores, memories, times, cpus),
                    "T-Coffee": overall_score(tcoffee_info, sp_scores, memories, times, cpus),
                    "ClustalOmega": overall_score(clustalo_info, sp_scores, memories, times, cpus),
                    "PRANK": overall_score(prank_info, sp_scores, memories, times, cpus)}
        
        bar_plots = {"Memories": create_bar_plot(memories, "RAM Memory Value (MB)", "RAM Usage"),
                     "Times": create_bar_plot(times, "Time of Execution (s)", "Execution Times"),
                     "SP-Scores": create_bar_plot(sp_scores, "SP-Score", "SP-Scores"),
                     "CPU": create_bar_plot(cpus, "Total CPU Usage (%)", "CPU Usage"),
                     "Overall": create_bar_plot(o_scores, "Overall Score", "Overall Scores")}
        
        # Obtain the best MSA software for each parameter
        # Get the MSA software(s) with the least memory used
        mem = [m for m in memories if all(memories[v] >= memories[m] for v in memories)]
        mem_str = ", ".join(mem)
        # Get the MSA software(s) with the shortest execution time(s)
        tim = [t for t in times if all(times[v] >= times[t] for v in times)]
        time_str = ", ".join(tim)
        # Get the MSA software(s) with the least cpu usage
        cpu = [c for c in cpus if all(cpus[v] >= cpus[c] for v in cpus)]
        cpu_str = ", ".join(cpu)
        # Get the MSA software(s) with the highest SP-Score(s) 
        sp = [s for s in sp_scores if all(sp_scores[v] <= sp_scores[s] for v in sp_scores)]
        sp_str = ", ".join(sp)
        # Get the MSA software(s) with the highest SP-Score(s) 
        overall = [o for o in o_scores if all(o_scores[v] <= o_scores[o] for v in o_scores)]
        overall_str = ", ".join(overall)
        
        # Create a new folder to add all files generated by the MSA softwares
        filename = os.path.basename(sys.argv[1]).split(".")[0]
        new_folder = f"MSA_Info_{filename}"
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        # Move all these files to the folder
        for file in msa_files.values():
            if os.path.exists(file):
                shutil.move(file, os.path.join(new_folder, os.path.basename(file)))
        # Move all bar plot files to the folder
        for file in bar_plots.values():
            if os.path.exists(file):
                shutil.move(file, os.path.join(new_folder, os.path.basename(file)))
        
        # Remove .dnd file
        # Get the directory where I'm running my script
        current_dir = os.getcwd()
        dnd_file = os.path.join(current_dir, f"{filename}.dnd")
        os.remove(dnd_file)

        # Create a text file containing the results of the process
        with open(f"MSA_Info_{filename}.log", "w") as file:
            file.write(f"\nMSA Software with the least RAM usage: {mem_str}\n\n")
            file.write(f"Fastest MSA Software(s): {time_str}\n\n")
            file.write(f"MSA Software with the least CPU usage: {cpu_str}\n\n")
            file.write(f"MSA Software(s) with the best alignments: {sp_str}\n\n")
            file.write(f"MSA Software(s) with the best overall score: {overall_str}\n\n\n")
            file.write(create_table(sp_scores, memories, times, cpus, o_scores))
        # Move the results file to the "MSA_Info" folder
        file_path = os.path.join(new_folder, f"MSA_Info_{filename}.log")
        if os.path.exists(f"MSA_Info_{filename}.log"):
            shutil.move(f"MSA_Info_{filename}.log", file_path)
        
        # Display log results as output
        with open(file_path, "r") as file:
            print(file.read())