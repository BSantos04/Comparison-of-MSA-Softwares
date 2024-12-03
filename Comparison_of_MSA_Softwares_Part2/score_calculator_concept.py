def hierarchical_score(ref_aln, *other_alns):
    """
    Calculates the hierarchical score for an aligned file based on it's SP-Score, used memory and time of execution.
    It compares this parameters with of the other alignments and do a rule of three for those parameters, making next the sum of all.
    
    Parameters:
        ref_aln: Alignment which the function is going to calculate the hierarchical score.
        *other_alns: Any other alignment that is gonna be used just for the score calculation of the reference alignment.
    
    Returns:
        h_score: The hierarchical score calculated for the reference alignment.

    """
    # Define the sp-score values for every alignment
    ref_sp_score = class_sp.sp_score(ref_aln)
    all_sp_score = [class_sp.sp_score(x) for x in other_alns]
    all_sp_score.append(ref_sp_score)
    
    # Since there's the possibility that the values can be negative (like, very negative), we create an offset to normalize them
    min_sp = min(all_sp_score)
    offset = abs(min_sp) + 1
    
    # Based on the determined offset, we change all the values
    new_sp = [x + offset for x in all_sp_score]
    ref_sp_score += offset
    
    # Using the rule of three, we calculate the SP-Score value for the reference alignment that will be used to calculate the hierarchical score
    h_sp = (ref_sp_score/max(all_sp_score))*3
    
    # Define the memory values for every alignment
    ref_memory = get_memory_and_time(ref_aln).memory
    all_memories = [get_memory_and_time(x).memory for x in other_alns]
    all_memories.append(ref_memory)
    
    #Calculate the memory value for the reference alignment for the hierarchical score using the rule of three
    h_memory = (ref_memory/max(all_memories)) 
    
    # Define the execution time values for every alignment
    ref_memory = get_memory_and_time(ref_aln).exec_time
    all_times = [get_memory_and_time(x).exec_time for x in other_alns]
    all_times.append(ref_times)
    
    #Calculate the execution time value for the reference alignment for the hierarchical score using the rule of three
    h_time = (ref_time/max(all_times)) 
    
    #Calculate the hierarchical score
    h_score = round(h_sp + h_memory + h_time, 2)
    
    return h_score
    