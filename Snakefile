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
        directory(f"MSA_Info/{dataset_basename}")  # Use pre-extracted dataset name

rule build_docker:
    output:
        "msa_analysis.built"
    shell:
        "docker build -t msa_analysis . && touch {output}"

rule run_analysis:
    input:
        dataset=dataset,
        matrix=matrix
    output:
        directory(f"MSA_Info/{dataset_basename}")  # Use the extracted dataset name
    shell:
        """
        echo "Running docker with dataset: {input.dataset} and matrix: {input.matrix}"
        docker run --rm -v $(pwd)/datasets:/app/datasets -v $(pwd)/scoring_matrices:/app/scoring_matrices -v $(pwd):/app msa_analysis python3 /app/code4pipeline.py /app/{input.dataset} /app/{input.matrix}
        """
    