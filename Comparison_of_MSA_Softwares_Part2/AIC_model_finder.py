import sys, os, gzip, re

def AIC_model_finder(aligned_file, nt=1):
    """
    This function runs the IQ-TREE2 command line using an aligned FASTA file and returns the best substitution AIC 
    model for the respective file.
    
    Arguments:
        .aligned_file: a FASTA file containing biological sequences, all aligned.
    
    Returns:
        .best_AIC_model: the best AIC substitution model for the aligned file to proceed with a phylogenetic analysis.
        
    Summary:
        .The function specify the expected path to the zipped file containing all the best substitution models for 
        the aligned file.
        .Then, it runs the IQ-TREE2 command line, which will generate some files, including the previous one, 
        which will be zipped.
        .After unziping it, we use RegEx to define the needed patterns in order to find the best AIC model, which 
        probably will be written in the file. If not, it will return a message saying the model wasn`t found, 
        otherwise it will return the model as a string.
    """
    aligned_file_directory = os.path.dirname(os.path.abspath(aligned_file))
    model_file = f"{aligned_file}.model"
    model_file_path = os.path.join(aligned_file_directory, f"{model_file}.gz")

    os.system(f"iqtree2 -s {aligned_file} -m MFP -nt {nt}")

    pattern = re.compile(r"^best_model_AIC:\s+(\S+)")
    best_AIC_model = None
    
    with gzip.open(model_file_path, "rt") as unzip:
        for line in unzip:
            match = pattern.search(line)
            if match:
                best_AIC_model = match.group(1)
                break
            
    if best_AIC_model is not None:
        return best_AIC_model
    else:
        return "AIC model not found!"

if __name__=="__main__":
    if len(sys.argv)<2 or len(sys.argv)>3:
        print("Usage: python3 {path/to/script.py} {path/to/aligned/file.FASTA} {number of threads (optional)}")
    elif len(sys.argv)==3:
        print(AIC_model_finder(sys.argv[1], sys.argv[2]))
    else:
        print(AIC_model_finder(sys.argv[1]))
    