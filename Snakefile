import os

def uniquify(path):
    """
    Summary: 
        Checks if the path of the folder exists. Beacuase the folder creation is dynamic, it fllows the folder path with the respective numeration.

    Parameters:
        path: Path of the folder.

    Returns:
        path: Path of the new folder.
    """
    counter = 1
    new_path = path

    while os.path.exists(new_path):
        new_path = f"{path} ({counter})"  
        counter += 1

    return new_path


try:
    # Get dataset and matrix from the config
    dataset = config.get("dataset")
    matrix = config.get("matrix")

    # If either dataset or matrix is not provided, raise an error
    if not dataset or not matrix:
        raise ValueError("Error: Missing required parameters.\nUsage: snakemake --config dataset={path/to/dataset} matrix={path/to/scoring/matrix}")

    # Extract the dataset basename
    dataset_basename = os.path.basename(dataset).split(".")[0]
    # Specify the folder name
    folder = f"MSA_Info_{dataset_basename}"
    # Create unique path for the folder
    unique_output_folder = uniquify(folder)

except ValueError as e:
    print(e)
    raise SystemExit(1)

# Define the final target
rule all:
    input:
        unique_output_folder

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
        directory(unique_output_folder)  
    shell:
        """
        echo "Running docker with dataset: {input.dataset} and matrix: {input.matrix}"
        docker run --user $(id -u):$(id -g) --rm \
            -v $(pwd)/datasets:/app/datasets \
            -v $(pwd)/scoring_matrices:/app/scoring_matrices \
            -v $(pwd):/app \
            msa_info python3 /app/code4pipeline.py /app/{input.dataset} /app/{input.matrix}

        """

