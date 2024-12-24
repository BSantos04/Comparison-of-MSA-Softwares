import pandas as pd

def create_table(sp_scores, memories, times, o_scores):
    """
    Summary: 
        Creates a table with every MSA software and their respective scores for every parameter.

    Parameters:
        sp_scores: Dictionary containing the SP-Scores of every MSA software.
        memories: Dictionary containing the RAM usage of every MSA software.
        times: Dictionary containing the execution time of every MSA software.
        o_scores: Dictionary containing the overall scores of every MSA software.

    Returns:
        table: The table object without the indexes of each list parameter (MSA softwares)

    """
    # Create lists containing the values of each parameter dictionary
    sp_list = list(sp_scores.values())
    memories_list = list(memories.values())
    times_list = list(times.values())
    o_list = list(o_scores.values())
    
    # Create a dictionary containing the data that will be used to create the table
    d = {
         "MSA Software": ["MAFFT", "MUSCLE", "T-Coffee", "ClustalOmega", "PRANK"],
         "SP-Score": sp_list,
         "RAM Usage (MB)": memories_list,
         "Time (s)": times_list,
         "Overall Score": o_list}
    
    # Convert the data into a dataframe
    df = pd.DataFrame(data=d)
    
    # Create the table object removing the indexes
    table = df.to_string(index=False) + "\n"
    
    return table