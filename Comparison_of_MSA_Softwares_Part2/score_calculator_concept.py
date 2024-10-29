def score_calculator(main_alignment_info, *alignement_info):
    tree_score = (tree_construction(main_alignment_info.output_file)*3)/max(tree_construction(main_alignment_info), tree_construction(alignment_info))
    memory_score = ((1/main_alignment_info.memory)*2)/min(1/main_alignment_info.memory, 1/alignment_info.memory)
    speed_score = main_alignment_info.speed/min(main_alignment_info.speed, alignment_info.speed)
    
    return round(tree_score + memory_score + speed_score, 2)


    
    
    