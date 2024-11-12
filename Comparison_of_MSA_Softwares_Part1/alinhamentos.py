import os, sys

fasta_input = sys.argv[1]

def mafft(ficheiro_input, ficheiro_output):
    comando = ["mafft --auto", ficheiro_input]
    os.system(comando)
    print(f"Alinhamento com o MAFFT está gravado como {ficheiro_output}")

def muscle(ficheiro_input, ficheiro_output):
    comando = ["muscle -in", ficheiro_input, "-out", ficheiro_output]
    os.system(comando)
    print(f"Alinhamento com o MUSCLE gravado como {ficheiro_output}")

def tcoffee(ficheiro_input, ficheiro_output):
    comando = ["t_coffee -in", ficheiro_input, "-output fasta_aln -outfile", ficheiro_output]
    os.system(comando)
    print(f"Alinhamento com o T-Coffee gravado como {ficheiro_output}")

def clustalomega(ficheiro_input, ficheiro_output):
    comando = ["clustalo -i", ficheiro_input, "-o", ficheiro_output, "--outfmt fasta"]
    os.system(comando)
    print(f"Alinhamento com o Clustal Omega gravado como {ficheiro_output}")


ficheiro_outputs = {
    "mafft": "aligned_mafft.fasta",
    "muscle": "aligned_muscle.fasta",
    "tcoffee": "aligned_tcoffee.fasta",
    "clustalomega": "aligned_clustalo.fasta",
}


mafft(fasta_input, ficheiro_outputs["mafft"])
muscle(fasta_input, ficheiro_outputs["muscle"])
tcoffee(fasta_input, ficheiro_outputs["tcoffee"])
clustalomega(fasta_input, ficheiro_outputs["clustalo"])