try:
    # Get dataset and matrix from the config
    dataset = config.get("dataset")
    matrix = config.get("matrix")

    # If either dataset or matrix is not provided, raise a ValueError with the following usage message
    if not dataset or not matrix:
        raise ValueError("Error: Missing required parameters.\nUsage: snakemake --config dataset={path/to/dataset} matrix={path/to/scoring/matrix}")

except ValueError as e:
    # If there's a ValueError, print the message and stop the execution
    print(e)
    # Exit with a non-zero status to indicate an error
    raise SystemExit(1)  

rule all:
    input:
        directory="MSA_Info_{dataset|basename}"

rule build_docker:
    shell:
        "docker build -t msa_analysis . && touch {output}"

rule run_analysis:
    input:
        dataset=dataset,
        matrix=matrix
    output:
        directory="MSA_Info_{dataset|basename}"
    shell:
        """
        echo "Running docker with dataset: {input.dataset} and matrix: {input.matrix}"
        docker run --rm -v $(pwd)/datasets:/app/datasets -v $(pwd)/scoring_matrices:/app/scoring_matrices -v $(pwd):/app msa_analysis python3 /app/code4pipeline.py /app/{input.dataset} /app/{input.matrix}
	"""
