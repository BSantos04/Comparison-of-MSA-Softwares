import os, sys

fasta_input = sys.argv[1]

def mafft(ficheiro_input, ficheiro_output):
    comando = f"mafft --auto {ficheiro_input} > {ficheiro_output}"
    os.system(comando)
    print(f"Alinhamento com o MAFFT está gravado como {ficheiro_output}")

def muscle(ficheiro_input, ficheiro_output):
    comando = f"muscle -align {ficheiro_input} -output {ficheiro_output}"
    os.system(comando)
    print(f"Alinhamento com o MUSCLE gravado como {ficheiro_output}")

def tcoffee(ficheiro_input, ficheiro_output):
    comando = f"t_coffee -in {ficheiro_input} -output fasta_aln -outfile {ficheiro_output}"
    os.system(comando)
    print(f"Alinhamento com o T-Coffee gravado como {ficheiro_output}")

def clustalomega(ficheiro_input, ficheiro_output):
    comando = f"clustalo -i {ficheiro_input} -o {ficheiro_output} --outfmt fasta"
    os.system(comando)
    print(f"Alinhamento com o Clustal Omega gravado como {ficheiro_output}")