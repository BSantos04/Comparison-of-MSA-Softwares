import sys
from Bio import AlignIO
from itertools import combinations, product

def get_score_matrix(match=1, mismatch=-1):
    """
    Summary:
        This function defines the score matrix fr the SP-Score calculation for all nucleotide pairs in the alignment
        
    Parameters:
        -match=1: Defines that each pair match equals to +1 point in the score matrix.
        -mismatch=-1: Defines that each pair mismatch equals to -1 point in the score matrix
    
    Returns:
        -score_matrix: The score matrix generated by the function.
    """
    #Define the nucleotides that will be part of the pair comparison and an empty dictionary that will contain 
    #all possible pair combinations for the defined nucleotides and their respective score
    bases = ["A", "T", "G", "C"]
    score_matrix = {}
    
    #Filling the score matrix with all possible pair combinations, defining each pair with equal nucelotides with 
    #a +1 score and each mismatch with a -1 score
    for i, j in product(bases, repeat=2):
        if i == j:
            score_matrix[(i, j)] = match
        else:
            score_matrix[(i, j)] = mismatch
    return score_matrix

def sp_score(aligned_file, score_matrix, gap_penalty=-1):
    """
    Summary:
        This function is a try out in order to simulate the Sum-of-Pairs Score calculation for the alignments.
        
    Arguments:
        -aligned_file: Aligned file created in the previous steps.
        -score_matrix: The score matrix defined in the previous function that will help us to give a score for each 
         nucleotide match or mismatch.
        -gap_penalty=-1: Defined penalty for each gap that will appear in the alignment.
        
    Returns:
        -score: SP-Score calculated by the function.
    """
    #Converting every characters of the aligned file upper case
    with open(aligned_file, "r+") as file:
        
        #Read the file content
        seqs = file.read()
        
        #Converting the file content to upper case
        seqs = seqs.upper()
        
        #Go back to the start of the file
        file.seek(0)
        
        #Overwrite the upper case content in the file
        file.write(seqs)
        
        #Remove the previous content of the file and close it
        file.truncate()
        file.close()
        
    #Create an AlignIO object for the aligned file used and an "empty" integer object for the score to be calculated
    alignment = AlignIO.read(aligned_file, "fasta")
    score = 0
    
    #Determine the number of sequences in the alignment
    num_seqs = len(alignment)
    
    #Search for all characters in each aligned sequence and define the pair variables for the score calculation
    for (i, j) in combinations(range(num_seqs), 2):
        for pos in range(alignment.get_alignment_length()):
            n1 = alignment[i][pos]
            n2 = alignment[j][pos]
                
            #SP-Score calculation based on the defined parameters for each nucleotide pair and/or character
            if n1 == "-" or n2 == "-":
                score += gap_penalty
            elif (n1, n2) in score_matrix:
                score += score_matrix[(n1, n2)]
            elif (n2, n1) in score_matrix:
                score += score_matrix[(n2, n1)]
            else:
                score += gap_penalty 
    return score

if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("Usage: python3 {path/to/script.py} {path/to/aligned/file.FASTA}")
    else:
        score_matrix = get_score_matrix()
        print(sp_score(sys.argv[1], score_matrix))
                        
                    
                
            
