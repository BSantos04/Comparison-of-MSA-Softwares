import time
import os
import subprocess
import sys
import psutil
import shutil
from Bio import AlignIO
import matplotlib.pyplot as plt
import pandas as pd
import math

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
    
    def probcons(self, input_file):
        """
        Runs the ProbCons alignment command on the input file and returns the aligned file along with memory and execution time.
        
        Parameters:
            input_file: Input FASTA file that contains the sequences to be aligned.
        
        Returns:
            aligned_file: Path to the file aligned by the command line.
            memory_used: Memory used during the execution of ProbCons.
            exec_time: Time taken for the execution of CProbCons.
        """
        # Get the first name of the file based on the input file name
        filename = input_file.split(".")[0]
        # Define the command line to run the software ProbCons
        command = f"probcons {input_file} > {filename}_probcons_aln.fasta"
                
        # Get execution time, used memory and CPU usage for that software
        memory_used, exec_time, cpu_used = self.track_usage(command)
                
        # Get the directory which the output file will be written
        pwd = os.getcwd()
        aligned_file = os.path.join(pwd, f"{filename}_probcons_aln.fasta")
        
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
         "MSA Software": ["MAFFT", "MUSCLE", "T-Coffee", "ProbCons"],
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

def t_test(values):
    """
    Summary: 
        Identifies the value in a list that is most significantly different from the mean 
        using a one-sample t-test approximation.

    Parameters:
        values: A list of numerical values to evaluate.

    Returns:
        best_value: The value that is most significantly different from the mean.
    """
    # Calculate the mean of the list
    mean_value = sum(values) / len(values)
    
    # Calculate the standard deviation
    variance = sum((x - mean_value) ** 2 for x in values) / (len(values) - 1)
    std_dev = math.sqrt(variance)
    
    # If std_dev is zero, than all the values of the list are the same, so we just pick one to return
    if std_dev == 0:
        return values[0]
    else:
        # Perform t-tests to compare each value against the mean
        t_stats = []
        for value in values:
            # Calculate t-statistic for each value
            t_stat = (value - mean_value) / std_dev
            t_stats.append(t_stat)
        
        # Calculate p-values based on t-statistics (one-sample t-test approximation)
        p_values = [2 * (1 - math.erf(abs(t) / math.sqrt(2))) for t in t_stats]
        
        # Determine the "best" value based on the lowest p-value
        min_p_value = min(p_values)
        best_value_index = p_values.index(min_p_value)
        best_value = values[best_value_index]
        
        return best_value


# Just ensuring the code is only executed when the script is run as a standalone program.
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 {path/to/sequences/file.fasta} {path/to/scoring/matrix/file}")
    else:
        # Creating instances for the classes using the needed parameters
        spscore = SPScore(sys.argv[2])
        msa = msa_softwares()
        
        # Create arrays to store every parameter value from the 5 attempts
        all_memories = {"MAFFT": [], "MUSCLE": [], "T-Coffee": [], "ProbCons": []}
        all_times = {"MAFFT": [], "MUSCLE": [], "T-Coffee": [], "ProbCons": []}
        all_cpus = {"MAFFT": [], "MUSCLE": [], "T-Coffee": [], "ProbCons": []}
        all_sp_scores = {"MAFFT": [], "MUSCLE": [], "T-Coffee": [], "ProbCons": []}
        
        # Start running every MSA software 5 times
        for i in range(5):
            print(f"Run {i + 1}...")
            
            # Get info from all MSA softwares
            mafft_info = msa.mafft(sys.argv[1])
            muscle_info = msa.muscle(sys.argv[1])
            tcoffee_info = msa.tcoffee(sys.argv[1])
            probcons_info = msa.probcons(sys.argv[1])
            
            # Create a dictionary to store the path for every alignment
            msa_files = {"MAFFT": mafft_info[0],
                        "MUSCLE": muscle_info[0],
                        "T-Coffee": tcoffee_info[0],
                        "ProbCons": probcons_info[0]}
            
            # Calculate SP-Score for each software
            mafft_sp_score = spscore.sp_score(mafft_info[0])
            muscle_sp_score = spscore.sp_score(muscle_info[0])
            tcoffee_sp_score = spscore.sp_score(tcoffee_info[0])
            clustalo_sp_score = spscore.sp_score(probcons_info[0])
            
            # Store all objects from every attempt for every MSA software
            all_memories["MAFFT"].append(mafft_info[1])
            all_times["MAFFT"].append(mafft_info[2])
            all_cpus["MAFFT"].append(mafft_info[3])
            all_sp_scores["MAFFT"].append(mafft_sp_score)
        
            all_memories["MUSCLE"].append(muscle_info[1])
            all_times["MUSCLE"].append(muscle_info[2])
            all_cpus["MUSCLE"].append(muscle_info[3])
            all_sp_scores["MUSCLE"].append(muscle_sp_score)
        
            all_memories["T-Coffee"].append(tcoffee_info[1])
            all_times["T-Coffee"].append(tcoffee_info[2])
            all_cpus["T-Coffee"].append(tcoffee_info[3])
            all_sp_scores["T-Coffee"].append(tcoffee_sp_score)
        
            all_memories["ProbCons"].append(probcons_info[1])
            all_times["ProbCons"].append(probcons_info[2])
            all_cpus["ProbCons"].append(probcons_info[3])
            all_sp_scores["ProbCons"].append(clustalo_sp_score)
            
            # Print the results for this run
            print(f"\nResults for Run {i + 1}:")
            print(f"MAFFT - SP-Score: {mafft_sp_score}, Memory: {mafft_info[1]} KB, Time: {mafft_info[2]} s, CPU: {mafft_info[3]}%")
            print(f"MUSCLE - SP-Score: {muscle_sp_score}, Memory: {muscle_info[1]} KB, Time: {muscle_info[2]} s, CPU: {muscle_info[3]}%")
            print(f"T-Coffee - SP-Score: {tcoffee_sp_score}, Memory: {tcoffee_info[1]} KB, Time: {tcoffee_info[2]} s, CPU: {tcoffee_info[3]}%")
            print(f"ProbCons - SP-Score: {clustalo_sp_score}, Memory: {probcons_info[1]} KB, Time: {probcons_info[2]} s, CPU: {probcons_info[3]}%\n")

        
        # Create dictionaries to store the best value of each parameter for every MSA software based on the t-test
        best_memories = {}
        best_times = {}
        best_cpus = {}
        best_sp_scores = {}
        
        # Obtain the best values of each parameter based on the t-test and store in his respective dictionary
        for tool in all_memories.keys():
            best_memories[tool] = t_test(all_memories[tool])
            best_times[tool] = t_test(all_times[tool])
            best_cpus[tool] = t_test(all_cpus[tool])
            best_sp_scores[tool] = t_test(all_sp_scores[tool])

        # Calculate overall score for every MSA software based on the best values of every parameter
        o_scores = {}
        for tool in all_memories.keys():
            normalized_sp_score = (best_sp_scores[tool] * 5) / max(best_sp_scores.values())
            normalized_memory = (1 / best_memories[tool]) / (1 / min(best_memories.values()))
            normalized_time = (1 / best_times[tool]) / (1 / min(best_times.values()))
            normalized_cpu = (1 / best_cpus[tool]) / (1 / min(best_cpus.values()))
            o_scores[tool] = normalized_sp_score + normalized_memory + normalized_time + normalized_cpu

        # Create barplots containing the info of every MSA software
        bar_plots = {"Memories": create_bar_plot(best_memories, "RAM Memory Value (KB)", "RAM Usage"),
                     "Times": create_bar_plot(best_times, "Time of Execution (s)", "Execution Times"),
                     "SP-Scores": create_bar_plot(best_sp_scores, "SP-Score", "SP-Scores"),
                     "CPU": create_bar_plot(best_cpus, "Total CPU Usage (%)", "CPU Usage"),
                     "Overall": create_bar_plot(o_scores, "Overall Score", "Overall Scores")}
        
        # Obtain the best MSA software for each parameter
        # Get the MSA software(s) with the least memory used
        mem = [m for m in best_memories if all(best_memories[v] >= best_memories[m] for v in best_memories)]
        mem_str = ", ".join(mem)
        # Get the MSA software(s) with the shortest execution time(s)
        tim = [t for t in best_times if all(best_times[v] >= best_times[t] for v in best_times)]
        time_str = ", ".join(tim)
        # Get the MSA software(s) with the least cpu usage
        cpu = [c for c in best_cpus if all(best_cpus[v] >= best_cpus[c] for v in best_cpus)]
        cpu_str = ", ".join(cpu)
        # Get the MSA software(s) with the highest SP-Score(s) 
        sp = [s for s in best_sp_scores if all(best_sp_scores[v] <= best_sp_scores[s] for v in best_sp_scores)]
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
        # Create a text file containing the results of the process
        with open(f"MSA_Info_{filename}.log", "w") as file:
            file.write(f"\nMSA Software with the least RAM usage: {mem_str}\n\n")
            file.write(f"Fastest MSA Software(s): {time_str}\n\n")
            file.write(f"MSA Software with the least CPU usage: {cpu_str}\n\n")
            file.write(f"MSA Software(s) with the best alignments: {sp_str}\n\n")
            #file.write(f"MSA Software(s) with the best overall score: {overall_str}\n\n\n")
            file.write(create_table(best_sp_scores, best_memories, best_times, best_cpus, o_scores))
        # Move the results file to the "MSA_Info" folder
        file_path = os.path.join(new_folder, f"MSA_Info_{filename}.log")
        if os.path.exists(f"MSA_Info_{filename}.log"):
            shutil.move(f"MSA_Info_{filename}.log", file_path)
        
        # Display log results as output
        with open(file_path, "r") as file:
            print(file.read())