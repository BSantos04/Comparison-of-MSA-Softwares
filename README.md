# Comparison of MSA Softwares

## Description

This project makes a comparative analysis of four of the most used Multiple Sequence Alignment Softwares of our choice, taking into consideration RAM usage (in kB),CPU usage (in %), execution time (in seconds), SP-Score and an overall scoring function made by us.

Among the MSA softwares, we selected: MAFFT, MUSCLE, KAlign2 and ClustalOmega. 

This analysis is made with the purpose of finding out which one is the best as an overall, under certain circunstances (depending on the used dataset), and helps the user to find out the best software to fulfill his needs.

## Requirements
- Docker v26.1.3
- Snakemake v8.27.1

## Installation
```
git clone https://github.com/BSantos04/Comparison-of-MSA-Softwares.git
```

## Usage
Before running the pipeline, don't forget to give give yourself permission to use Docker.

Try this:
```
sudo usermod -aG docker $USER
newgrp docker
```
Now you can run the pipeline without any issues:
```
snakemake --config dataset={path/to/dataset} matrix={path/to/scoring/matrix}
```

### Example
```
snakemake --config dataset=datasets/dna_seqs/sample.fasta matrix=scoring_matrices/NUCLEOTIDE
```
```
snakemake --config dataset=datasets/protein_seqs/sample.fasta matrix=scoring_matrices/BLOSUM62
```

Disclaimer: BLOSUM matrices must be used with protein sequences, while the NUCLEOTIDE matrix is used with DNA alignments.

### Check Results
```
ls MSA_Info_{basename_of_the_dataset}
```

### Expected Outputs
- Barplot containing the final RAM usage values of every software (RAM_Usage.png)

- Barplot containing the final CPU usage values of every software (CPU_Usage.png)

- Barplot containing the final SP-Score values of every software (SP-Scores.png)

- Barplot containing the final execution time values of every software (Execution_Times.png)

- Barplot containing the final overall score values of every software (Overall_Scores.png)

- Log file summarizing the final results (MSA_Info_{dataset_basename}.log)

## Credits
https://www.docker.com/

https://snakemake.readthedocs.io/en/stable/ 

https://www.drive5.com/muscle/ 

https://mafft.cbrc.jp/alignment/server/index.html 

http://www.clustal.org/omega/ 

https://msa.sbc.su.se/cgi-bin/msa.cgi 

