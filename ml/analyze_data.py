"""
Day 3 - Repository Analytics Engine
====================================

This script reads raw repository metadata collected from GitHub, performs
data cleaning (deduplication & handling missing values), prints key analytics
summaries (including averages and ranking), and generates visually engaging charts.

Functions included:
1. load_data(file_path): Loads and cleans the CSV dataset.
2. print_summary(df): Prints the analytical summary to the terminal.
3. generate_charts(df): Generates and saves visual charts in docs/charts/.
4. main(): Standard entry point coordinating the analysis workflow.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    """
    Loads GitHub repository data from a CSV file, cleans it, and returns a DataFrame.
    
    Steps:
    1. Check if the CSV dataset exists.
    2. Read it into a pandas DataFrame.
    3. Drop duplicates based on the 'full_name' column (since topics search can overlap).
    4. Fill missing language cells with 'Unknown'.
    5. Convert 'stars' and 'forks' columns into numeric values.
    """
    # Verify the target file exists before trying to open it
    if not os.path.exists(file_path):
        print(f"Error: Dataset file not found at '{file_path}'")
        return None
        
    print(f"Reading dataset from {file_path}...")
    df = pd.read_csv(file_path)
    
    # Deduplicate repositories by their unique full_name (e.g. 'facebook/react')
    # This prevents counting the same repository multiple times in our statistics.
    df_unique = df.drop_duplicates(subset='full_name', keep='first').copy()
    
    # Fill any empty cells in the 'language' column with 'Unknown'
    df_unique['language'] = df_unique['language'].fillna('Unknown')
    
    # Convert stars and forks columns to numeric, replacing invalid values with 0
    df_unique['stars'] = pd.to_numeric(df_unique['stars'], errors='coerce').fillna(0).astype(int)
    df_unique['forks'] = pd.to_numeric(df_unique['forks'], errors='coerce').fillna(0).astype(int)
    
    return df_unique

def print_summary(df):
    """
    Prints a formatted summary of repository metrics to the terminal.
    
    Metrics printed:
    - Total unique repositories count
    - Top 10 languages by repo count
    - Top 10 repositories by stars
    - Top 10 repositories by forks
    - Average stars per repository
    - Average forks per repository
    """
    if df is None or df.empty:
        print("No repository data available to summarize.")
        return

    total_repos = len(df)
    avg_stars = df['stars'].mean()
    avg_forks = df['forks'].mean()

    # Print summary header
    print("=" * 65)
    print("                 GITHUB REPOSITORY ANALYTICS SUMMARY            ")
    print("=" * 65)
    print(f"Total Unique Repositories : {total_repos}")
    print(f"Average Stars per Repo    : {avg_stars:,.2f}")
    print(f"Average Forks per Repo    : {avg_forks:,.2f}")
    print("-" * 65)

    # Calculate Top 10 Languages
    print("Top 10 Programming Languages:")
    top_languages = df['language'].value_counts().head(10)
    for idx, (lang, count) in enumerate(top_languages.items(), 1):
        print(f"  {idx:2d}. {lang:<15} : {count} repositories")
    print("-" * 65)

    # Calculate Top 10 Repositories by Stars
    print("Top 10 Repositories by Stars:")
    top_stars = df.sort_values(by='stars', ascending=False).head(10)
    for idx, (_, row) in enumerate(top_stars.iterrows(), 1):
        print(f"  {idx:2d}. {row['full_name']:<40} | {row['stars']:,} stars | {row['language']}")
    print("-" * 65)

    # Calculate Top 10 Repositories by Forks
    print("Top 10 Repositories by Forks:")
    top_forks = df.sort_values(by='forks', ascending=False).head(10)
    for idx, (_, row) in enumerate(top_forks.iterrows(), 1):
        print(f"  {idx:2d}. {row['full_name']:<40} | {row['forks']:,} forks | {row['language']}")
    print("=" * 65)

def generate_charts(df, output_dir="docs/charts"):
    """
    Generates and saves three visual charts in the target output folder.
    
    Charts generated:
    1. docs/charts/top_languages.png (Horizontal bar chart of languages count)
    2. docs/charts/top_repositories_by_stars.png (Vertical bar chart of stars)
    3. docs/charts/top_repositories_by_forks.png (Vertical bar chart of forks)
    """
    if df is None or df.empty:
        print("No repository data available to generate charts.")
        return

    # Create target directory if it doesn't already exist
    os.makedirs(output_dir, exist_ok=True)

    # Apply global styling for professional visual appeal
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['text.color'] = '#2c3e50'
    plt.rcParams['axes.labelcolor'] = '#2c3e50'
    plt.rcParams['xtick.color'] = '#2c3e50'
    plt.rcParams['ytick.color'] = '#2c3e50'

    # -----------------------------------------------------------------
    # Chart 1: Top Languages (top_languages.png)
    # -----------------------------------------------------------------
    top_languages = df['language'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    n_langs = len(top_languages)
    # Create a nice gradient of teal colors
    lang_colors = [plt.cm.GnBu(0.4 + 0.55 * (i / (n_langs - 1 if n_langs > 1 else 1))) for i in range(n_langs)]
    bars = ax.barh(top_languages.index[::-1], top_languages.values[::-1], color=lang_colors, edgecolor='none', height=0.65)
    
    ax.set_title("Top 10 Programming Languages by Repo Count", fontsize=15, fontweight='bold', pad=20, color='#1a252f')
    ax.set_xlabel("Number of Repositories", fontsize=11, labelpad=10)
    
    # Visual improvements: light vertical gridlines, remove frames/spines
    ax.xaxis.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax.set_axisbelow(True)
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)

    # Add numeric count label next to each bar
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.15, bar.get_y() + bar.get_height()/2, f' {int(width)}', 
                va='center', ha='left', fontsize=10, fontweight='semibold', color='#475569')

    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "top_languages.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"Saved language chart: {chart1_path}")

    # -----------------------------------------------------------------
    # Chart 2: Top Repositories by Stars (top_repositories_by_stars.png)
    # -----------------------------------------------------------------
    top_stars = df.sort_values(by='stars', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(12, 7))
    
    n_stars = len(top_stars)
    # Gradient of purple/indigo colors
    star_colors = [plt.cm.Purples(0.45 + 0.5 * (i / (n_stars - 1 if n_stars > 1 else 1))) for i in range(n_stars)]
    
    bars = ax.bar(top_stars['repo_name'], top_stars['stars'], color=star_colors, edgecolor='none', width=0.55)
    
    ax.set_title("Top 10 Repositories by Star Count", fontsize=15, fontweight='bold', pad=20, color='#1a252f')
    ax.set_ylabel("Stars", fontsize=11, labelpad=10)
    ax.set_xlabel("Repository Name", fontsize=11, labelpad=10)
    
    # Format Y axis values to include thousands comma separators
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda val, pos: f"{int(val):,}"))
    
    # Visual improvements: light horizontal gridlines, remove spines
    ax.yaxis.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax.set_axisbelow(True)
    plt.xticks(rotation=25, ha='right', fontsize=9)

    # Add text labels on top of the bars (using "k" shorthand for large numbers)
    max_star_val = max(top_stars['stars']) if len(top_stars) > 0 else 1
    for bar in bars:
        height = bar.get_height()
        label_text = f"{height/1000:.1f}k" if height >= 1000 else f"{int(height)}"
        ax.text(bar.get_x() + bar.get_width()/2., height + (max_star_val * 0.012), 
                label_text, ha='center', va='bottom', fontsize=9, fontweight='semibold', color='#475569')

    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "top_repositories_by_stars.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"Saved stars chart: {chart2_path}")

    # -----------------------------------------------------------------
    # Chart 3: Top Repositories by Forks (top_repositories_by_forks.png)
    # -----------------------------------------------------------------
    top_forks = df.sort_values(by='forks', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(12, 7))
    
    n_forks = len(top_forks)
    # Gradient of orange/red colors
    fork_colors = [plt.cm.Oranges(0.4 + 0.55 * (i / (n_forks - 1 if n_forks > 1 else 1))) for i in range(n_forks)]
    
    bars = ax.bar(top_forks['repo_name'], top_forks['forks'], color=fork_colors, edgecolor='none', width=0.55)
    
    ax.set_title("Top 10 Repositories by Fork Count", fontsize=15, fontweight='bold', pad=20, color='#1a252f')
    ax.set_ylabel("Forks", fontsize=11, labelpad=10)
    ax.set_xlabel("Repository Name", fontsize=11, labelpad=10)
    
    # Format Y axis values
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda val, pos: f"{int(val):,}"))
    
    # Visual improvements
    ax.yaxis.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax.set_axisbelow(True)
    plt.xticks(rotation=25, ha='right', fontsize=9)

    # Add text labels on top of the bars
    max_fork_val = max(top_forks['forks']) if len(top_forks) > 0 else 1
    for bar in bars:
        height = bar.get_height()
        label_text = f"{height/1000:.1f}k" if height >= 1000 else f"{int(height)}"
        ax.text(bar.get_x() + bar.get_width()/2., height + (max_fork_val * 0.012), 
                label_text, ha='center', va='bottom', fontsize=9, fontweight='semibold', color='#475569')

    plt.tight_layout()
    chart3_path = os.path.join(output_dir, "top_repositories_by_forks.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(f"Saved forks chart: {chart3_path}")

def main():
    """
    Main entry point of the analytics script.
    
    Loads the repository dataset, displays statistics summary in the terminal,
    and exports formatted analytical charts to disk.
    """
    csv_file = "data/github_repositories.csv"
    
    # Load and clean the repository data
    df = load_data(csv_file)
    
    if df is not None:
        # Print analytics to console
        print_summary(df)
        
        # Build and save visual charts
        generate_charts(df)
        print("\nRepository analytics completed successfully!")

if __name__ == "__main__":
    main()
