# Comparison of MSA Softwares

## Description

This project make a comparative analysis of four of the most used Multiple Sequence Alignment softwares of our choice, having in consideration RAM usage (in kB),CPU usage (in %), execution time (in seconds), SP-Score and an overall scoring function made by us.

Among the MSA softwares, we selected: MAFFT, MUSCLE, KAlign2 and ClustalOmega. 

This analysis is made with the purpose of finding out which one is the best as an overall certain circunstances (depending on the used dataset), and helps the user to find out the best software to fulfill his needs.

## Requirements
- Docker
- Snakemake

## Usage
```
snakemake --config dataset={path/to/dataset} matrix={path/to/scoring/matrix}
```

### Example
```
snakemake --config dataset=datasets/sample.fasta matrix=scoring_matrices/BLOSUM62
```

### Check Results
```
ls MSA_Info_{basename_of_the_dataset}
```

## Credits
https://www.docker.com/
https://snakemake.readthedocs.io/en/stable/ 
https://www.drive5.com/muscle/ 
https://mafft.cbrc.jp/alignment/server/index.html 
http://www.clustal.org/omega/ 
https://msa.sbc.su.se/cgi-bin/msa.cgi 

## Preparação

For everything to run smoothly, we will be working inside a docker. To acquire a docker image with the necessary programs, we will pull the last version of the image from this project's [DockerHub](https://hub.docker.com/r/stargazernex/lbproject/tags).
```
docker pull stargazernex/lbproject:<Version>
```
Remember to swap <Version> for the last version available in the DockerHub. Alternatively, you may also use the Dockerfile in this repository
