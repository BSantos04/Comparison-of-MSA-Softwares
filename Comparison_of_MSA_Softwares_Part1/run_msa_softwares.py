import os
import sys


def mafft(input_file):
    """
    Summary:
        This function runs the MAFFT command line in order to proceed with
        the alignemnt of the sequences in the input file
        using the software.
    
    Parameters:
        input_file: Input FASTA file that contains the sequences to be aligned.
    
    Returns:
        aligned_file: Path to the file aligned by the command line.

    """
    # Specify the first name that we are going to use to specify the output file later
    filename = input_file.split(".")[0]
    # Run the command line for the MAFFT software
    os.system(f"mafft {input_file} > {filename}_mafft_aln.fasta")
    # Get the directory which the output file will be written
    pwd = os.getcwd()
    # Get the path to the output file using the directory obtain previously
    aligned_file = os.path.join(pwd, f"{filename}_mafft_aln.fasta")
    return aligned_file


def muscle(input_file):
    """
    Summary:
        This function runs the MUSCLE command line in order to proceed with
        the alignemnt of the sequences in the input file
        using the software.
    
    Parameters:
        input_file: Input FASTA file that contains the sequences to be aligned.
    
    Returns:
        aligned_file: Path to the file aligned by the command line.

    """
    # Specify the first name that we are going to use to specify the output file later
    filename = input_file.split(".")[0]
    # Run the command line for the MUSCLE software
    os.system(f"muscle -align {input_file} -output {filename}_muscle_aln.fasta")
    # Get the directory which the output file will be written
    pwd = os.getcwd()
    # Get the path to the output file using the directory obtain previously
    aligned_file = os.path.join(pwd, f"{filename}_muscle_aln.fasta")
    return aligned_file


def tcoffee(input_file):
    """
    Summary:
        This function runs the T-Coffee command line in order to proceed with
        the alignemnt of the sequences in the input file
        using the software.
    
    Parameters:
        input_file: Input FASTA file that contains the sequences to be aligned.
    
    Returns:
        aligned_file: Path to the file aligned by the command line.

    """
    # Specify the first name that we are going to use to specify the output file later
    filename = input_file.split(".")[0]
    # Run the command line for the T-Coffee software
    os.system(f"t_coffee -in {input_file} -output fasta_aln -outfile {filename}_tcoffee_aln.fasta")
    # Get the directory which the output file will be written
    pwd = os.getcwd()
    # Get the path to the output file using the directory obtain previously
    aligned_file = os.path.join(pwd, f"{filename}_tcoffee_aln.fasta")
    return aligned_file


def clustalomega(input_file):
    """
    Summary:
        This function runs the ClustalOmega command line in order to proceed
        with the alignemnt of the sequences in the input file
        using the software.
    
    Parameters:
        input_file: Input FASTA file that contains the sequences to be aligned.
    
    Returns:
        aligned_file: Path to the file aligned by the command line.

    """
    # Specify the first name that we are going to use to specify the output file later
    filename = input_file.split(".")[0]
    # Run the command line for the ClustalOmega software
    os.system(f"clustalo -i {input_file} -o {filename}_clustalo_aln.fasta --outfmt fasta")
    # Get the directory which the output file will be written
    pwd = os.getcwd()
    # Get the path to the output file using the directory obtain previously
    aligned_file = os.path.join(pwd, f"{filename}_clustalo_aln.fasta")
    return aligned_file


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 {path/to/script.py} {path/to/input/file.fasta}")
    else:
        mafft_aln = mafft(sys.argv[1])
        muscle_aln = muscle(sys.argv[1])
        tcoffee_aln = tcoffee(sys.argv[1])
        clustalo_aln = clustalomega(sys.argv[1])
        with open(mafft_aln, "r") as seqs:
            print(seqs.read())
        with open(muscle_aln, "r") as seqs:
            print(seqs.read())
        with open(tcoffee_aln, "r") as seqs:
            print(seqs.read())
        with open(clustalo_aln, "r") as seqs:
            print(seqs.read())
