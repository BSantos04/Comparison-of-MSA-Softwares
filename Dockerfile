# Using snakemake as base image
FROM snakemake/snakemake:v7.32.4

# Install alignment requirements via conda
RUN mamba install mafft=7.520 -c bioconda
RUN mamba install conda-forge::biopython
RUN mamba install -y -c bioconda -c conda-forge clustalo=1.2.4
RUN mamba install -y -c bioconda -c conda-forge muscle=5.1
RUN mamba install -y -c bioconda -c conda-forge t-coffee=11.0.8
# RUN mamba install -y -c bioconda -c conda-forge prank=170427
RUN mamba install -y -c bioconda -c conda-forge famsa=2.2.3

# Install Others Requirements
RUN mamba install -y -c bioconda -c conda-forge psutil=5.9.0

# Install pandas, matplotlib
RUN mamba install -y -c conda-forge pandas=2.1.2
RUN mamba install -y -c conda-forge matplotlib=3.6.0

WORKDIR /App
COPY . /App