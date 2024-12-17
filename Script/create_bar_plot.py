import matplotlib.pyplot as plt
import os

def create_bar_plot(info_dict, ylabel, title):
    """
    Summary: 
        Creates a bar plot with the values displayed on top of each bar.

    Parameters:
        info_dict: Dictionary with software names as keys and parameter values as values.
        ylabel: Label for the y-axis of the bar plot.
        title: Title of the bar plot.

    Returns:
        plot_file_path: The absolute path to the saved bar plot image file.
    """
    # Extract keys and values based on the given dictionary
    labels = list(info_dict.keys())
    values = list(info_dict.values())
    
    # Create the bar plot
    fig, ax = plt.subplots()
    bars = ax.bar(labels, values, color="blue", width=0.5)
    
    # Add labels and a title
    ax.set_xlabel("MSA Softwares")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    # Display the value on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # x position
            height,  # y position
            f'{height:.2f}',  # Text to display with two decimal points
            ha='center',  # Horizontal alignment
            va='bottom',  # Vertical alignment
            fontsize=10,  # Font size
            color="black"  # Text color
        )
    
    # Saving the plot into a file
    filename = "_".join(title.split())
    plot_file_path = os.path.abspath(f"{filename}.png")
    plt.tight_layout()  # Adjust layout to prevent overlapping
    plt.savefig(plot_file_path)
    
    # Free up memory by closing the plot
    plt.close()
    
    return plot_file_path  