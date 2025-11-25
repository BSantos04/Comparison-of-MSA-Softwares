import os
import matplotlib.pyplot as plt
import pandas as pd
import math

class analysis:
    def __init__(self):
        pass
    
    def normalized_score(self, value, info_dict, choice=None):
        """
        Summary:
            Normalizes a given value based on a dictionary of values.
            - For SP-Score (higher is better), we scale to [0,5].
            - For RAM, Time, and CPU (lower is better), we scale to [0,1].

        Parameters:
            value: The value to be normalized.
            info_dict: Dictionary containing all values for this specific parameter.
            choice: If None, SP-Score normalization is used (higher is better).
                    Otherwise, inverse normalization is applied (lower is better).

        Returns:
            normalized_score: The normalized value.
        """
        
        scores = list(info_dict.values())
        
        if choice is None:
            # Normalize SP-Score (higher is better) → range [0,5]
            min_spscore = min(scores)
            max_spscore = max(scores)
            if max_spscore != min_spscore:  
                normalized_score = 5 * (value - min_spscore) / (max_spscore - min_spscore)
            else:
                normalized_score = 5  # If all SP-Scores are the same
        
        else:
            # Normalize RAM, Time, and CPU (lower is better) → range [0,1]
            epsilon = 1e-10  
            min_score = min(scores) + epsilon
            max_score = max(scores) + epsilon
            value += epsilon

            normalized_score = 1 - (value - min_score) / (max_score - min_score)
        
        return normalized_score
    

    def create_bar_plot(self, info_dict, ylabel, title):
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
                f'{height:.3f}',  # Text to display with two decimal points
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
        
    def create_table(self, sp_scores, memories, times, cpus, o_scores, info_dict):
        """
        Summary: 
            Creates a table with every MSA software and their respective scores for every parameter.

        Parameters:
            sp_scores: Dictionary containing the SP-Scores of every MSA software.
            memories: Dictionary containing the RAM usage of every MSA software.
            times: Dictionary containing the execution time of every MSA software.
            cpus: Dictionary containing the CPU usage of every MSA software.
            o_scores: Dictionary containing the overall scores of every MSA software.

        Returns:
            table: The table object without the indexes of each list parameter (MSA softwares)

        """
        # Create lists containing the values of each parameter dictionary
        sp_list = list(sp_scores.values())
        memories_list = list(memories.values())
        times_list = list(times.values())
        cpu_list = list(cpus.values())
        o_list = list(o_scores.values())
        
        # Create a dictionary containing the data that will be used to create the table
        d = {
            "MSA Software": list(info_dict.keys()),
            "SP-Score": sp_list,
            "RAM Usage": memories_list,
            "Time": times_list,
            "CPU Usage": cpu_list,
            "Overall Score": o_list}
        
        # Convert the data into a dataframe
        df = pd.DataFrame(data=d)
        
        # Create the table object removing the indexes
        table = df.to_string(index=False) + "\n"
        
        return table

    def t_test(self, values):
        """
        Summary: 
            Identifies the value in a list that is most significantly different from the mean 
            using a one-sample t-test approximation.

        Parameters:
            values: A list of numerical values to evaluate.

        Returns:
            best_value: The value that is most significantly different from the mean.
        """
        # Calculate the mean of the list
        mean_value = sum(values) / len(values)
        
        # Calculate the standard deviation
        variance = sum((x - mean_value) ** 2 for x in values) / (len(values) - 1)
        std_dev = math.sqrt(variance)
        
        # If std_dev is zero, than all the values of the list are the same, so we just pick one to return
        if std_dev == 0:
            return values[0]
        else:
            # Perform t-tests to compare each value against the mean
            t_stats = []
            for value in values:
                # Calculate t-statistic for each value
                t_stat = (value - mean_value) / std_dev
                t_stats.append(t_stat)
            
            # Calculate p-values based on t-statistics (one-sample t-test approximation)
            p_values = [2 * (1 - math.erf(abs(t) / math.sqrt(2))) for t in t_stats]
            
            # Determine the "best" value based on the lowest p-value
            min_p_value = min(p_values)
            best_value_index = p_values.index(min_p_value)
            best_value = values[best_value_index]
            
            return best_value