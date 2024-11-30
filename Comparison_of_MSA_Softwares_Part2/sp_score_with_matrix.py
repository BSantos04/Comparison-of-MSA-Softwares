import sys
import os
from Bio import AlignIO

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
            Tuple of ((row_id, col_id), parse_matrix(matrix_cell)).
        """
        # Reading and splitting all the lines/rows of the matrix
        rows = (line.rstrip().split() for line in file)
        
        # Extracting the headers/column identifiers of the matrix
        header = next(rows)
        
        # Processing rows, specifying each row 
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
            Dictionary representing the scoring matrix with tuple keys (row_id, col_id) and integer values.
        """
        with open(matrix_file) as f:
            # Use read_scoring_matrix to parse the file and convert it to a dictionary
            matrix = dict(self.read_scoring_matrix(f))
            # Convert all values to integers
            return {key: int(value) for key, value in matrix.items()}

    def affine_gap_penalty(self, gap_len, gapO=-6, gap_ext=-1):
        """
        Calculates the affine gap penalty score for a given gap length.
        
        Parameters:
            gap_len: Length of the gap in an aligned sequence.
            gapO: Gap opening penalty (default: -5).
            gap_ext: Gap extension penalty per unit length (default: -2).
        
        Returns:
            The affine gap penalty score.
        """
        return gapO + gap_len * gap_ext

    def pairwise_score(self, seq1, seq2):
        """
        Calculates the pairwise score of two aligned sequences using the scoring matrix and gap penalties.
        
        Parameters:
            seq1: First sequence of the pair.
            seq2: Second sequence of the pair.
        
        Returns:
            The total pairwise score for the given sequences.
        """
        score = 0
        gap1, gap2 = 0, 0

        # Loop through pairs of characters from the two sequences
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

        if gap1 > 0:
            score += self.affine_gap_penalty(gap1)
        if gap2 > 0:
            score += self.affine_gap_penalty(gap2)

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
                sp_score += self.pairwise_score(seq1, seq2)

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
        scoring_matrix = sys.argv[2]
        if not os.path.exists(aligned_file):
            print(f"Error: File '{aligned_file}' does not exist.")
        else:
            class_sp = SPScore(scoring_matrix)
            score = class_sp.sp_score(aligned_file)
            print(f"SP-Score of the alignment: {score}")
