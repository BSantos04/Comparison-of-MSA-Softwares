import os
import sys
import shutil
import msa_softwares
import SPScore
import overall_score
import create_bar_plot
import create_table

# Just ensuring the code is only executed when the script is run as a standalone program.
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 {path/to/sequences/file.fasta} {path/to/scoring/matrix/file}")
    else:
        # Creating instances for the classes using the needed parameters
        spscore = SPScore.SPScore(sys.argv[2])
        msa = msa_softwares.msa_softwares()
        
        # Run all the MSA softwares
        mafft_info = msa.mafft(sys.argv[1])
        muscle_info = msa.muscle(sys.argv[1])
        tcoffee_info = msa.tcoffee(sys.argv[1])
        clustalo_info = msa.clustalomega(sys.argv[1])
        prank_info = msa.prank(sys.argv[1])
        
        # Get all returned objects from each alignment (aligned file, used memory and execution time)
        mafft_aln, mafft_memory, mafft_time = mafft_info
        muscle_aln, muscle_memory, muscle_time = muscle_info
        tcoffee_aln, tcoffee_memory, tcoffee_time = tcoffee_info
        clustalo_aln, clustalo_memory, clustalo_time = clustalo_info
        prank_aln, prank_memory, prank_time = prank_info
        
        # Get dictionaries
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
        
        sp_scores = {"MAFFT": spscore.sp_score(mafft_aln),
                    "MUSCLE": spscore.sp_score(muscle_aln),
                    "T-Coffee": spscore.sp_score(tcoffee_aln),
                    "ClustalOmega": spscore.sp_score(clustalo_aln), 
                    "PRANK": spscore.sp_score(prank_aln)}
        
        o_scores = {"MAFFT": overall_score.overall_score(mafft_info, sp_scores, memories, times),
                    "MUSCLE": overall_score.overall_score(muscle_info, sp_scores, memories, times),
                    "T-Coffee": overall_score.overall_score(tcoffee_info, sp_scores, memories, times),
                    "ClustalOmega": overall_score.overall_score(clustalo_info, sp_scores, memories, times),
                    "PRANK": overall_score.overall_score(prank_info, sp_scores, memories, times)}
        
        bar_plots = {"Memories": create_bar_plot.create_bar_plot(memories, "RAM Memory Values (MB)", "Used RAM Memories"),
                     "Times": create_bar_plot.create_bar_plot(times, "Times of Execution (s)", "Execution Times"),
                     "SP-Scores": create_bar_plot.create_bar_plot(sp_scores, "SP-Scores", "SP-Scores"),
                     "Overall": create_bar_plot.create_bar_plot(o_scores, "Overall Scores", "Overall Scores")}
        
        # Obtain the best MSA software for each parameter
        # Get the MSA software(s) with the least memory used
        print()
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
        
        # Print the table containing the scores 
        print()
        print(create_table.create_table(sp_scores, memories, times, o_scores))
        
        # Create a new folder to add all files generated by the MSA softwares
        filename = os.path.basename(sys.argv[1]).split(".")[0]
        new_folder = f"MSA_Info_{filename}"
        if not os.path.exists(f"MSA_Info_{filename}"):
            os.mkdir(f"MSA_Info_{filename}")
        # Move all these files to the folder
        for file in msa_files.values():
            if os.path.exists(file):
                shutil.move(file, os.path.join(f"MSA_Info_{filename}", os.path.basename(file)))
        # Move all bar plot files to the folder
        for file in bar_plots.values():
            if os.path.exists(file):
                shutil.move(file, os.path.join(f"MSA_Info_{filename}", os.path.basename(file)))
        
        # Remove .dnd file
        # Get the directory where I'm running my script
        current_dir = os.path.dirname(__file__)
        dnd_file = os.path.join(current_dir, f"{filename}.dnd")
        os.remove(dnd_file)
        
        # Create a text file containing the table with all the scores
        with open("results.log", "w") as file:
            file.write(create_table.create_table(sp_scores, memories, times, o_scores))
        # Move the table file to the "MSA_Info" folder
        if os.path.exists("results.log"):
            shutil.move("results.log", os.path.join(new_folder, "results.log"))