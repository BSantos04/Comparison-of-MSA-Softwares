import sys
import os
from Bio import AlignIO


def read_scoring_matrix(file, parse_matrix=lambda x: x):
    """
    Summary:
        This function transforms a BLAST format matrix into a Python tuple matrix object containing all the possible pairs
        of proteins/nucleotides and their respective scores.
    
    Parameters:
        file: Input file cotaining the BLAST format matrix.
        parse_matrix: Default parameter that allows the function to transform the values in the matrix. By deafult,
        it returns the value unchanged.

    Returns:
        ((row_id, col_id), parse_matrix(matrix_cell)): This command-line represents the Python matrix object "returned"
        by the function. Since we are generating the scoring matrix by processing the matrix file row by row and cell by cell,
        we can't use the 'return' method, so instead we are using the 'yield' method.

    """
    # Reading and spliting all the lines/rows of the matrix
    rows = (line.rstrip().split() for line in file)
    
    # Extracting the headers/column identifiers of the matrix
    header = next(rows)
    
    # Processing rows, specifying each row identifier
    for row in rows:
        row_id = row[0]
        
        # Iterating through matrix cells, pairing each column identifier with its corresponding matrix value
        for col_id, matrix_cell in zip(header, row[1:]):
            yield ((row_id, col_id), parse_matrix(matrix_cell))

# Opens the matrix file and runs the previous function, turining the generated matrix object into a dictionary object


with open(sys.argv[2]) as f:
    matrix = dict(read_scoring_matrix(f))
    scoring_matrix = {key: int(value) for key, value in matrix.items()}


def affine_gap_penalty(gap_len, gapO=-5, gap_ext=-2):
    """
    Summary:
        This function takes the gap length of an aligned sequence and calculates the affine gap penalty score for that line of gaps.
    
    Parameters:
        gap_len: Gap length if an aligned sequence
        gap0=-6: An int object specifying the penalty for the opening gap (-6).
        gap_exp=-1: An int object specifying the penalty for each following gap on the gap sequence (including the opening gap) (-1).
    
    Returns:
        gapO + gap_len * gap_ext: The affine gap penalty score for that specific gap sequence.

    """
    return gapO + gap_len * gap_ext


def pairwise_score(seq1, seq2):
    """
    Summary:
        This function calculates the pairwise score of two sequences of an aligned file based on the generated matrix and
        the gap penalties previously defined.
    
    Parameters:
        seq1: First sequence of the pair.
        seq2: Seconde sequence of the pair.
    
    Returns:
        score: Resulting score for that pair of sequences.

    """
    # Creating the int objects for the score and consecutive gaps in seq1 and seq2 to track these values
    score = 0
    gap1, gap2 = 0, 0

    # Looping through pairs of characters from the two sequences
    for a, b in zip(seq1, seq2):
        # If both sites have gaps, the score will ignore it
        if a == "-" and b == "-":
            continue
        # Calculating the score if either character of the two sequences is a gap based on the next characters
        if a == "-" or b == "-":
            if a == "-":
                gap1 += 1
                if gap2 > 0:
                    score += affine_gap_penalty(gap2)
                    gap2 = 0
            if b == "-":
                gap2 += 1
                if gap1 > 0:
                    score += affine_gap_penalty(gap1)
                    gap1 = 0
        # Calculating the score for each match and mismatch between the two seqs...
        else:
            # If a character is a gap
            if gap1 > 0:
                score += affine_gap_penalty(gap1)
                gap1 = 0
            if gap2 > 0:
                score += affine_gap_penalty(gap2)
                gap2 = 0
            # If neither character is a gap
            score += scoring_matrix.get((a, b), 0)
            
    # Applying gap penalty for any gap that extended to the end of the sequences
    if gap1 > 0:
        score += affine_gap_penalty(gap1)
    if gap2 > 0:
        score += affine_gap_penalty(gap2)

    return score


def sp_score(aligned_file):
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
    
    # Determine the number of sequences on the algned file and creating an int object to handle the sp_score value
    num_seqs = len(alignment)
    sp_score = 0

    # Calculates the pairwise score for every pair of sequences of the file
    for i in range(num_seqs):
        for j in range(i + 1, num_seqs):
            # We are just ensuring that every character of the sequences are upper case
            seq1 = str(alignment[i].seq).upper()
            seq2 = str(alignment[j].seq).upper()
            # Add all the obtained pairwise score values to the sp_score object
            sp_score += pairwise_score(seq1, seq2)
    
    return sp_score


if __name__ == "__main__":
    """
    Summary:
        This function orquestrates the entire process of the script and ensures that the code is only executed when
        the script is run as a standalone program.
    """
    # Prints a message if the script command-line does not comply the number of parameters
    if len(sys.argv) != 3:
        print("Usage: python3 script.py aligned_file.fasta scoring_matrix")
    else:
        aligned_file = sys.argv[1]
        if not os.path.exists(aligned_file):
            print(f"Error: File '{aligned_file}' does not exist.")
        else:
            score = sp_score(aligned_file)
            print(f"SP-Score of the alignment: {score}")
