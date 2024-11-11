import sys, os, re, math

def find_AIC_value(aligned_file, nt=1):
    """
    Summary:
        This function will run IQ-TREE2 command-line in order to generate an .iqtree file and find the AIC score init
        for an aligned FASTA file.
        
    Arguments:
        -aligned_file: Aligned FASTA file
        -nt: Number of threads used in order to run IQ-TREE2 command-line
        
    Returns:
        -best_aic_score: The best AIC score found in the .iqtree file for that alignment
    """
    
    #Define the path of the targeted file (in this case the .iqtree file containing all the AIC scores for that alignemnt)
    aligned_file_directory = os.path.dirname(os.path.abspath(aligned_file))
    iqtree_file_path = os.path.join(aligned_file_directory, f"{aligned_file}.iqtree")

    #Running the iqtree2 command-line that will create the needed file
    os.system(f"iqtree2 -s {aligned_file} -m MFP -nt {nt}")

    #Define the pattern in order to find the line with the needed scores
    pattern = re.compile(r"^(\S+)\s+-?\d+\.\d+\s+(\d+\.\d+)\s")
    best_aic_score = float("inf")
    
    #Open the .iqtree file and searching line by line the lowest AIC score found using the defined pattern
    #We determine the best model according to AIC by the one with the lowest score
    with open(iqtree_file_path, "r") as aic_file:
        for line in aic_file:
            match = pattern.search(line)
            if match:
                aic_score = float(match.group(2))
                if aic_score < best_aic_score:
                    best_aic_score = aic_score
            
        return best_aic_score

def AICw_calculator(aic_score, *aic_scores):
    """
    Summary:
        This function will calculate the AIC weigth for a certain alignment
    
    Parameters:
        -aic_score: The obtained AIC score from the previous function of the target alignment
        -*aic_scores: All the AIC scores obtained from all the alignments
        
    Returns:
        -aicw_score: AIC wegth for the target alignment
    """

    #Create an array with all the obtained AIC values 
    aic_values = [aic_score] + list(aic_scores)
    
    #Determine the minimum value among all obtained AIC scores
    min_aic = min(aic_values)
    
    #Calculate the AICw for the analysed alignment
    aicw = math.exp(-0.5*(aic_score-min_aic))
    
    #Calculate the total AICw for normalization
    aicw_total = sum([math.exp(-0.5*(x-min_aic)) for x in aic_values])
        
    #Get the AICw score for the analysed alignemnt
    aicw_score = aicw/aicw_total
    
    return aicw_score
    
    
if __name__=="__main__":
    """
    Notei que existe proporcionalidade inversa entre os valores obtidos de AIC e AICw 
    Perguntar ao stor se não é melhor utilizar apenas os valores de AIC para determinar a qualidade dos alinhamentos
    """
    if len(sys.argv)<2 or len(sys.argv)>3:
        print("Usage: python3 {path/to/script.py} {path/to/aligned/file.FASTA} {number of threads (optional)}")
    elif len(sys.argv)==3:
        x = 18970.538
        y = 18000.71
        aic_score = find_AIC_value(sys.argv[1], sys.argv[2])
        print(AICw_calculator(aic_score, x, y))
    else:
        x = 20000
        y = 18900
        aic_score = find_AIC_value(sys.argv[1])
        print(AICw_calculator(aic_score, x, y))
    