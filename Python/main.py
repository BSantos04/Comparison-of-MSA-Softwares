from SPScore import SPScore
from msa_softwares import msa_softwares
from analysis import analysis
import argparse
import os
import shutil

def uniquify(path):
    """
    Summary: 
        Checks if the path of the folder exists and creates another one with a nmertion to identify.

    Parameters:
        path: Path of the folder.

    Returns:
        path: Path of the new folder
    """
    # Specify folder name and respective extension of the path
    folder, extension = os.path.splitext(path)
    # Define a counter for the number of the folder to be created
    counter = 1

    # Check if the path of the folder exists, and if so, it creates another folder, but with the numeration after
    while os.path.exists(path):
        path = folder + " (" + str(counter) + ")" + extension
        counter +=1

    # Creates the new folder
    os.makedirs(path)

    return path

# Just ensuring the code is only executed when the script is run as a standalone program.
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=str, help="Dataset containing the FASTA sequences that will be aligned by the MSA softwares.")
    parser.add_argument("matrix", type=str, help="Scoring matrix used to evaluate the SP-Score of each MSA software (ex.: BLOSUM62)")
    args = parser.parse_args()

    # Creating instances for the classes using the needed parameters
    sp = SPScore(args.matrix)
    msa = msa_softwares()
    an = analysis()
    
    # Create arrays to store every parameter value from the 5 attempts
    all_memories = {"MAFFT": [], "MUSCLE": [], "KAlign2": [], "ClustalOmega": [], "PRANK": []}
    all_times = {"MAFFT": [], "MUSCLE": [], "KAlign2": [], "ClustalOmega": [], "PRANK": []}
    all_cpus = {"MAFFT": [], "MUSCLE": [], "KAlign2": [], "ClustalOmega": [], "PRANK": []}
    all_sp_scores = {"MAFFT": [], "MUSCLE": [], "KAlign2": [], "ClustalOmega": [], "PRANK": []}
    
    # Start running every MSA software 5 times
    for i in range(5):
        print(f"Run {i + 1}...\n")
        
        # Get info from all MSA softwares

        mafft_info = msa.mafft(args.dataset)
        muscle_info = msa.muscle(args.dataset)
        clustalo_info = msa.clustalo(args.dataset)
        kalign2_info = msa.kalign2(args.dataset)
        prank_info = msa.prank(args.dataset)
        
        # Create a dictionary to store the path for every alignment, if they exist
        msa_files = {
            "MAFFT": mafft_info[0] if mafft_info else None,
            "MUSCLE": muscle_info[0] if muscle_info else None,
            "KAlign2": kalign2_info[0] if kalign2_info else None,
            "ClustalOmega": clustalo_info[0] if clustalo_info else None,
            "PRANK": prank_info[0] if prank_info else None
        }
        
        # Add parameters to respective dictionaries
        if mafft_info:
            mafft_sp_score = sp.sp_score(mafft_info[0])
            all_memories["MAFFT"].append(mafft_info[1])
            all_times["MAFFT"].append(mafft_info[2])
            all_cpus["MAFFT"].append(mafft_info[3])
            all_sp_scores["MAFFT"].append(mafft_sp_score)
        if muscle_info:
            muscle_sp_score = sp.sp_score(muscle_info[0])
            all_memories["MUSCLE"].append(muscle_info[1])
            all_times["MUSCLE"].append(muscle_info[2])
            all_cpus["MUSCLE"].append(muscle_info[3])
            all_sp_scores["MUSCLE"].append(muscle_sp_score)
        if kalign2_info:
            kalign2_sp_score = sp.sp_score(kalign2_info[0])
            all_memories["KAlign2"].append(kalign2_info[1])
            all_times["KAlign2"].append(kalign2_info[2])
            all_cpus["KAlign2"].append(kalign2_info[3])
            all_sp_scores["KAlign2"].append(kalign2_sp_score)
        if clustalo_info:
            clustalo_sp_score = sp.sp_score(clustalo_info[0])
            all_memories["ClustalOmega"].append(clustalo_info[1])
            all_times["ClustalOmega"].append(clustalo_info[2])
            all_cpus["ClustalOmega"].append(clustalo_info[3])
            all_sp_scores["ClustalOmega"].append(clustalo_sp_score)
        if prank_info:
            prank_sp_score = sp.sp_score(prank_info[0])
            all_memories["PRANK"].append(prank_info[1])
            all_times["PRANK"].append(prank_info[2])
            all_cpus["PRANK"].append(prank_info[3])
            all_sp_scores["PRANK"].append(prank_sp_score)

        # Print the results for this run
        print(f"\nResults for Run {i + 1}:")
        if mafft_info:
            print(f"MAFFT - SP-Score: {mafft_sp_score}, Memory: {mafft_info[1]} KB, Time: {mafft_info[2]} s, CPU: {mafft_info[3]}%")
        if muscle_info:
            print(f"MUSCLE - SP-Score: {muscle_sp_score}, Memory: {muscle_info[1]} KB, Time: {muscle_info[2]} s, CPU: {muscle_info[3]}%")
        if kalign2_info:
            print(f"KAlign2 - SP-Score: {kalign2_sp_score}, Memory: {kalign2_info[1]} KB, Time: {kalign2_info[2]} s, CPU: {kalign2_info[3]}%")
        if clustalo_info:
            print(f"ClustalOmega - SP-Score: {clustalo_sp_score}, Memory: {clustalo_info[1]} KB, Time: {clustalo_info[2]} s, CPU: {clustalo_info[3]}%\n")
        if prank_info:
            print(f"ClustalOmega - SP-Score: {prank_sp_score}, Memory: {prank_info[1]} KB, Time: {prank_info[2]} s, CPU: {prank_info[3]}%\n")

        # Eliminate the alignments if they exist
        for i in msa_files.values():
            if i and os.path.exists(i):
                os.remove(i)
    
    # Create dictionaries to store the best value of each parameter for every MSA software based on the t-test
    best_memories = {}
    best_times = {}
    best_cpus = {}
    best_sp_scores = {}
    
    # Obtain the best values of each parameter based on the t-test and store in his respective dictionary
    for i in all_memories.keys():
        best_memories[i] = an.t_test(all_memories[i])
        best_times[i] = an.t_test(all_times[i])
        best_cpus[i] = an.t_test(all_cpus[i])
        best_sp_scores[i] = an.t_test(all_sp_scores[i])

    # Calculate overall score for every MSA software based on the best values of every parameter
    o_scores = {}
    for j in best_memories.keys():
        normalized_sp_score = an.normalized_score(best_sp_scores[j], best_sp_scores)  
        normalized_memory = an.normalized_score(best_memories[j], best_memories, 1)  
        normalized_time = an.normalized_score(best_times[j], best_times, 1)  
        normalized_cpu = an.normalized_score(best_cpus[j], best_cpus, 1)  
        
        # Sum of all normalized values, max possible score is 8
        o_scores[j] = normalized_sp_score + normalized_memory + normalized_time + normalized_cpu


    # Create barplots containing the info of every MSA software
    bar_plots = {"Memories": an.create_bar_plot(best_memories, "RAM Memory Value (KB)", "RAM Usage"),
                    "Times": an.create_bar_plot(best_times, "Time of Execution (s)", "Execution Times"),
                    "SP-Scores": an.create_bar_plot(best_sp_scores, "SP-Score", "SP-Scores"),
                    "CPU": an.create_bar_plot(best_cpus, "Total CPU Usage (%)", "CPU Usage"),
                    "Overall": an.create_bar_plot(o_scores, "Overall Score", "Overall Scores")}
    
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
    filename = os.path.basename(args.dataset).split(".")[0]
    folder_name = f"MSA_Info_{filename}"
    # Make sure it creates a unique folder and doesnt overwrite the existing one
    new_folder = uniquify(folder_name)
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
        
    # Move all bar plot files to the folder
    for file in bar_plots.values():
        if os.path.exists(file):
            shutil.move(file, os.path.join(new_folder, os.path.basename(file)))
    
    # Create a text file containing the results of the process
    with open(f"MSA_Info_{filename}.log", "w") as file:
        file.write(f"\nMSA Software with the least RAM usage: {mem_str}\n\n")
        file.write(f"Fastest MSA Software(s): {time_str}\n\n")
        file.write(f"MSA Software with the least CPU usage: {cpu_str}\n\n")
        file.write(f"MSA Software(s) with the best alignments: {sp_str}\n\n")
        file.write(f"MSA Software(s) with the best overall score: {overall_str}\n\n\n")
        file.write(an.create_table(best_sp_scores, best_memories, best_times, best_cpus, o_scores, all_memories))
    # Move the results file to the "MSA_Info" folder
    file_path = os.path.join(new_folder, f"MSA_Info_{filename}.log")
    if os.path.exists(f"MSA_Info_{filename}.log"):
        shutil.move(f"MSA_Info_{filename}.log", file_path)
    
    # Display log results as output
    with open(file_path, "r") as file:
        print(file.read())