def score_calculator(main_alignment_info, *other_alignement_info):
    tree_score = (tree_construction(main_alignment_info.output_file)*3)/max(tree_construction(main_alignment_info), tree_construction(other_alignment_info))
    memory_score = ((1/main_alignment_info.memory)*2)/min(1/main_alignment_info.memory, 1/other_alignment_info.memory)
    exec_time_score = (1/main_alignment_info.exec_time)/min((1/main_alignment_info.exec_time), (1/other_alignment_info.exec_time))
    
    return round(tree_score + memory_score + exec_time_score, 2)


    
    
    