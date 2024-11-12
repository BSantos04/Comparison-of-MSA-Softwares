# Using snakemake as base image
FROM snakemake/snakemake:v7.32.4

# Install alignment requirements via conda
RUN mamba install mafft=7.520 -c bioconda
RUN mamba install -y -c bioconda -c conda-forge clustalo=1.2.4
RUN mamba install -y -c bioconda -c conda-forge muscle=5.1
RUN mamba install -y -c bioconda -c conda-forge modeltest-ng=0.1.7
RUN mamba install -y -c bioconda -c conda-forge t-coffee=11.0.8

# Install Others Requirements
RUN mamba install -y -c bioconda -c conda-forge raxml-ng=1.2.0
RUN mamba install -y -c bioconda -c conda-forge psutil=5.9.0


# Install python packages to create the final phylo trees
RUN pip install --force-reinstall -v "toyplot==1.0.3"
RUN pip install --force-reinstall -v "toytree==3.0.5"

WORKDIR /App
COPY . /App
