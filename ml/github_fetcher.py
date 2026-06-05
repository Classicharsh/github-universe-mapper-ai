"""
GitHub Repository Data Collector
================================

This script connects to the GitHub Search API to collect trending repositories 
for specific technology topics, extracts key attributes, and saves them to a CSV file.

Prerequisites
-------------
1. Ensure the virtual environment is activated.
2. Install the required dependencies:
   pip install -r requirements.txt

How to Run
----------
Run the script using python:
    python ml/github_fetcher.py
"""

import os
import time
import requests
import pandas as pd

# List of target technology topics to search for
SEARCH_TOPICS = [
    "react",
    "nextjs",
    "python",
    "machine-learning",
    "artificial-intelligence",
    "fastapi",
    "mongodb",
    "postgresql"
]

def fetch_repositories(topic, per_page=20):
    """
    Fetches repositories for a specific topic using the GitHub Search API.

    Parameters:
        topic (str): The keyword or topic to search for (e.g., 'fastapi').
        per_page (int): Number of repository records to return per page (default: 20).

    Returns:
        list: A list of dictionaries, where each dictionary represents a repository's metadata.
    """
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"topic:{topic}",
        "sort": "stars",
        "order": "desc",
        "per_page": per_page
    }
    
    # Github API Best Practice: Include a User-Agent header
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "GitHub-Universe-Mapper-AI-Data-Collector"
    }

    try:
        print(f"Fetching repositories for topic: {topic}...")
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 403:
            print(f"Warning: Rate limit or access restriction encountered for '{topic}' (Status code: 403).")
            # GitHub rate limit warning
            if "X-RateLimit-Reset" in response.headers:
                reset_time = int(response.headers["X-RateLimit-Reset"])
                sleep_duration = max(1, reset_time - int(time.time()))
                print(f"Rate limit resets in {sleep_duration} seconds.")
            return []
            
        response.raise_for_status()
        
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with GitHub API for topic '{topic}': {e}")
        return []

    try:
        data = response.json()
    except ValueError as e:
        print(f"Error parsing JSON response for topic '{topic}': {e}")
        return []

    repositories = []
    items = data.get("items", [])
    
    for repo in items:
        # Extract only the specified fields, with safety defaults
        repositories.append({
            "repo_name": repo.get("name"),
            "full_name": repo.get("full_name"),
            "description": repo.get("description"),
            "stars": repo.get("stargazers_count"),
            "forks": repo.get("forks_count"),
            "language": repo.get("language"),
            "created_at": repo.get("created_at"),
            "updated_at": repo.get("updated_at"),
            "repo_url": repo.get("html_url")
        })

    print(f"Successfully fetched {len(repositories)} repositories for topic: {topic}")
    return repositories


def save_to_csv(repositories, output_path):
    """
    Saves a list of repository metadata to a CSV file.

    Parameters:
        repositories (list): A list of dictionaries containing repository metadata.
        output_path (str): The target file path for the CSV output.
        
    Returns:
        bool: True if saved successfully, False otherwise.
    """
    if not repositories:
        print("No repository data to save.")
        return False

    try:
        # Create parent directories if they don't exist
        dir_name = os.path.dirname(output_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        df = pd.DataFrame(repositories)
        df.to_csv(output_path, index=False, encoding="utf-8")
        print(f"Dataset successfully saved to: {output_path}")
        print(f"Total records saved: {len(df)}")
        return True
        
    except Exception as e:
        print(f"Failed to save dataset to CSV file: {e}")
        return False


def main():
    all_repositories = []

    for topic in SEARCH_TOPICS:
        repos = fetch_repositories(topic)
        all_repositories.extend(repos)
        # Sleep to comply with GitHub Search API rate limits (up to 30 requests per minute without auth)
        time.sleep(2)

    output_file = "data/github_repositories.csv"
    save_to_csv(all_repositories, output_file)


if __name__ == "__main__":
    main()
