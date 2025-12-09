# Using snakemake as base image
FROM snakemake/snakemake:v7.32.4

# Create /msa directory
WORKDIR /msa
COPY datasets /msa/datasets
COPY scoring_matrices /msa/scoring_matrices
COPY Python /msa/Python

# Define a HOME directory so T-COFFEE doesn't tweek
ENV HOME=/msa
ENV HOME_4_TCOFFEE=/msa
ENV TMP=/msa/tmp 
RUN mkdir -p /msa/tmp

# Install alignment requirements via conda
RUN mamba install mafft=7.520 -c bioconda
RUN mamba install -y -c bioconda -c conda-forge clustalo=1.2.4
RUN mamba install -y -c bioconda -c conda-forge muscle=5.1
RUN mamba install -y -c bioconda -c conda-forge kalign2=2.04
RUN mamba install -y -c bioconda t-coffee=12.00.7fb08c2
RUN mamba install -y -c bioconda prank==v.170427

# Install Others Requirements
RUN mamba install -y -c bioconda -c conda-forge psutil=5.9.0
RUN pip install biopython matplotlib pandas