import SPScore
import sys 

def overall_score(ref_info, sp_dict, mem_dict, time_dict):
    """
    Summary:
        This function calculates the overall score for one alignment based on the SP-Score, memory and execution time values obtain.
    
    Parameters:
        ref_info: Information of the aligned that is going to be analyzed and we are calculating the overall score.
        sp_dict: A dictionary containing the values of all SP-Scores of all alignments.
        mem_dict: A dictionary containing the values of all used memories of all alignments.
        time_dict: A dictionary containing the values of all execution times of all alignments.
    
    Returns:
        score: Overall score for the reference alignment.

    """
    # Creating instances for the classes using the needed parameters
    spscore = SPScore.SPScore(sys.argv[2])
    
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
    normalized_spscore = (aln_spscore*5)/max(sp_scores)
    
    # Noramlize the memory value in order to correspond to our overall score
    normalized_memory = (1/memory)/(1/min(mems))
    
    # Normalize the execution time value in order to corresponf to our overall score
    normalized_time = ((1/exectime))/(1/min(times))
    
    # Calculate the score for the reference alignment
    score = normalized_spscore + normalized_memory + normalized_time
    
    return score