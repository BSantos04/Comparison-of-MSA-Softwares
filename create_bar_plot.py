import matplotlib.pyplot as plt
import os

def create_bar_plot(info_dict, ylabel, title):
    
    # Extract keys and values based on the given dictionary
    labels = list(info_dict.keys())
    values = list(info_dict.values())
    
    # Create the bar plot
    plt.bar(labels, values, color="blue", width=0.5)
    
    # Add labels and a title
    plt.xlabel("MSA Softwares")
    plt.ylabel(f"{ylabel}")
    plt.title(f"{title}")
    
    # Saving the plot into a file
    filename = "_".join(title.split())
    plot_file_path = os.path.abspath(f"{filename}.png")
    plt.savefig(plot_file_path)
    
    # Free up memory by closing the plot
    plt.close()
    
    return plot_file_path