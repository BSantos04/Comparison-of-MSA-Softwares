import time
import os
import subprocess
import sys
import psutil
from Bio import AlignIO


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
    
class SPScore:
    def __init__(self, matrix_file):
        """
        Initializes the scoring_matrix object and loads the scoring matrix.
        
        Parameters:
            matrix_file: Path to the scoring matrix file in BLAST format.
        """
        self.scoring_matrix = self._load_matrix(matrix_file)

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

    def _load_matrix(self, matrix_file):
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
    
def overall_score(ref_info, sp_dict, mem_dict, time_dict):
    
    # Get the aligned file path, used memory and execution time of the reference alignment
    aln, memory, exectime = ref_info
    
    # Create list for every values of SP-Scores, used memories and execution times
    sp_scores = list(sp_dict.values())
    mems = list(mem_dict.values())
    times = list(time_dict.values())
    
    # Get the SP-Score for the reference alignment
    aln_spscore = spscore.sp_score(aln)
    
    # Since the SP-Score values can be negative (like, very negative), we are gonna need to transform them first
    min_spscore = min(sp_scores)
    aln_spscore += min_spscore
    for i in range(len(sp_scores)):
        sp_scores[i] += min_spscore
    
    # Normalize the SP-Score value in order to correspond to our overall score 
    normalized_spscore = (aln_spscore*3.5)/max(sp_scores)
    
    # Noramlize the memory value in order to correspond to our overall score
    normalized_memory = (1/memory)/(1/min(mems))
    
    # Normalize the execution time value in order to corresponf to our overall score
    normalized_time = ((1/exectime)*0.5)/(1/min(times))
    
    # Calculate the score for the reference alignment
    score = normalized_spscore + normalized_memory + normalized_time
    
    return score
    
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
        
        # Get all returned objects from each alignment (aligned file, used memory and execution time)
        mafft_aln, mafft_memory, mafft_time = mafft_info
        muscle_aln, muscle_memory, muscle_time = muscle_info
        tcoffee_aln, tcoffee_memory, tcoffee_time = tcoffee_info
        clustalo_aln, clustalo_memory, clustalo_time = clustalo_info
        
        # Create a tuple containing all the info from all the sequences
        all_info = (mafft_info, muscle_info, tcoffee_info, clustalo_info)
        
        # Get a dictionary of each parameter value of every MSA software
        memories = {"MAFFT": mafft_memory,
                    "MUSCLE": muscle_memory,
                    "T-Coffee": tcoffee_memory,
                    "ClustalOmega": clustalo_memory}
        
        times = {"MAFFT": mafft_time,
                 "MUSCLE": muscle_time,
                 "T-Coffee": tcoffee_time,
                 "ClustalOmega": clustalo_time}
        
        sp_scores = {"MAFFT": spscore.sp_score(mafft_aln),
                    "MUSCLE": spscore.sp_score(muscle_aln),
                    "T-Coffee": spscore.sp_score(tcoffee_aln),
                    "ClustalOmega": spscore.sp_score(clustalo_aln)}
        
        o_scores = {"MAFFT": overall_score(mafft_info, sp_scores, memories, times),
                    "MUSCLE": overall_score(muscle_info, sp_scores, memories, times),
                    "T-Coffee": overall_score(tcoffee_info, sp_scores, memories, times),
                    "ClustalOmega": overall_score(clustalo_info, sp_scores, memories, times)}
        
        # Obtain the best MSA software for each parameter
        # Get the MSA software(s) with the least memory used
        mem = [m for m in memories if all(memories[v] >= memories[m] for v in memories)]
        mem_str = ", ".join(mem)
        print(f"MSA Software with the least RAM usage: {mem_str}")
        # Get the MSA software(s) with the shortest execution time(s)
        tim = [t for t in times if all(times[v] >= times[t] for v in times)]
        time_str = ", ".join(tim)
        print(f"Fastest MSA Software(s): {time_str}")
        # Get the MSA software(s) with the highest SP-Score(s) 
        sp = [s for s in sp_scores if all(sp_scores[v] <= sp_scores[s] for v in sp_scores)]
        sp_str = ", ".join(sp)
        print(f"MSA Software(s) with the best alignments: {sp_str}")
        # Get the MSA software(s) with the highest SP-Score(s) 
        overall = [o for o in o_scores if all(o_scores[v] <= o_scores[o] for v in o_scores)]
        overall_str = ", ".join(overall)
        print(f"MSA Software(s) with the best overall score: {overall_str}")
        
        print(str(memories.values()))
        print(str(times.values()))
        print(str(sp_scores.values()))
        print(str(o_scores.values()))