# Using snakemake as base image
FROM snakemake/snakemake:v7.32.4

# Install alignment requirements via conda
RUN mamba install mafft=7.520 -c bioconda
RUN mamba install -y -c bioconda -c conda-forge clustalo=1.2.4
RUN mamba install -y -c bioconda -c conda-forge muscle=5.1
RUN mamba install -y -c bioconda -c conda-forge kalign2=2.04

# Install Others Requirements
RUN mamba install -y -c bioconda -c conda-forge psutil=5.9.0
RUN pip install biopython matplotlib pandas


# Create /app directory
WORKDIR /app
COPY code4pipeline.py /app/
COPY datasets /app/datasets
COPY scoring_matrices /app/scoring_matrices

# Set entrypoint
CMD ["python3", "/app/code4pipeline.py"]
