import pandas as pd

def filter_pairs_analysis(high_winrate_file, analysis_results_file, output_file='filtered_analysis_results.csv'):
    """
    Filter pairs_analysis_results based on pairs found in high_winrate_pairs
    
    Parameters:
    high_winrate_file (str): Path to the high winrate pairs CSV file
    analysis_results_file (str): Path to the pairs analysis results CSV file
    output_file (str): Path for the output filtered CSV file
    """
    # Read the CSV files
    high_winrate_df = pd.read_csv(high_winrate_file)
    analysis_results_df = pd.read_csv(analysis_results_file)
    
    # Create a set of tuples containing the pairs from high_winrate_pairs
    high_winrate_pairs = set(zip(high_winrate_df['Asset1'], high_winrate_df['Asset2']))
    
    # Filter the analysis results
    filtered_results = analysis_results_df[
        analysis_results_df.apply(
            lambda row: (row['Asset1'], row['Asset2']) in high_winrate_pairs,
            axis=1
        )
    ]
    
    # Save the filtered results
    filtered_results.to_csv(output_file, index=False)
    
    print(f"Original number of pairs: {len(analysis_results_df)}")
    print(f"Number of high winrate pairs: {len(high_winrate_df)}")
    print(f"Number of filtered pairs: {len(filtered_results)}")
    
    return filtered_results

# Example usage
if __name__ == "__main__":
    filtered_df = filter_pairs_analysis(
        'high_winrate_pairs.csv',
        'pairs_analysis_results.csv',
        'filtered_analysis_results.csv'
    )