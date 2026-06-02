import requests
import pandas as pd
import time
import os

SEARCH_TOPICS = [
    "react",
    "nextjs",
    "python",
    "machine-learning",
    "artificial-intelligence",
    "langchain",
    "crewai",
    "fastapi",
    "django",
    "nodejs",
    "mongodb",
    "postgresql"
]

def fetch_repositories(topic, per_page=20):
    url = "https://api.github.com/search/repositories"

    params = {
        "q": f"topic:{topic}",
        "sort": "stars",
        "order": "desc",
        "per_page": per_page
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error fetching {topic}: {response.status_code}")
        return []

    data = response.json()
    repositories = []

    for repo in data.get("items", []):
        repositories.append({
            "search_topic": topic,
            "repo_name": repo.get("name"),
            "full_name": repo.get("full_name"),
            "description": repo.get("description"),
            "stars": repo.get("stargazers_count"),
            "forks": repo.get("forks_count"),
            "language": repo.get("language"),
            "topics": ", ".join(repo.get("topics", [])),
            "created_at": repo.get("created_at"),
            "updated_at": repo.get("updated_at"),
            "repo_url": repo.get("html_url")
        })

    return repositories


def main():
    all_repositories = []

    for topic in SEARCH_TOPICS:
        print(f"Fetching repositories for topic: {topic}")
        repos = fetch_repositories(topic)
        all_repositories.extend(repos)

        time.sleep(2)

    df = pd.DataFrame(all_repositories)

    os.makedirs("data", exist_ok=True)

    output_path = "data/github_repositories.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Dataset saved successfully: {output_path}")
    print(f"Total repositories collected: {len(df)}")


if __name__ == "__main__":
    main()
