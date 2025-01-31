import os

try:
    # Get dataset and matrix from the config
    dataset = config.get("dataset")
    matrix = config.get("matrix")

    # If either dataset or matrix is not provided, raise an error
    if not dataset or not matrix:
        raise ValueError("Error: Missing required parameters.\nUsage: snakemake --config dataset={path/to/dataset} matrix={path/to/scoring/matrix}")

    # Extract the dataset basename
    dataset_basename = os.path.basename(dataset)

except ValueError as e:
    print(e)
    raise SystemExit(1)

# Define the final target
rule all:
    input:
        f"MSA_Info_{dataset_basename}"  

rule build_docker:
    # Create a dummy file to track completion
    output:
        "msa_info.built"  
    # Build docker image
    shell:
        """
        docker build -t msa_info .
        touch msa_info.built  
        """

rule run_analysis:
    # Specify config parameters and ensure docker is built
    input:
        dataset=config["dataset"],  
        matrix=config["matrix"],
        docker_built="msa_info.built"   
    output:
        directory(f"MSA_Info_{dataset_basename}")  
    shell:
        """
        echo "Running docker with dataset: {input.dataset} and matrix: {input.matrix}"
        docker run --rm -v $(pwd)/datasets:/app/datasets -v $(pwd)/scoring_matrices:/app/scoring_matrices -v $(pwd):/app msa_info python3 /app/code4pipeline.py /app/{input.dataset} /app/{input.matrix}
        """

