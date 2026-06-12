#!/usr/bin/env python3
"""
Generate a CSV report of all your GitHub forks with detailed information.
Requires: pip install PyGithub
"""

import os
import csv
from datetime import datetime
from github import Github


def get_forks(username, token=None):
    """Fetch all forked repositories for a user."""
    if token:
        g = Github(token)
    else:
        g = Github()
    
    user = g.get_user(username)
    forks = []
    
    print(f"Fetching forks for {username}...")
    for repo in user.get_repos(type="owner"):
        if repo.fork:
            # Get original repo info
            original_repo = repo.source
            
            forks.append({
                'name': repo.name,
                'fork_url': repo.html_url,
                'original_url': original_repo.html_url,
                'description': repo.description or 'No description',
                'stars': original_repo.stargazers_count,
                'language': repo.language or 'N/A',
                'original_created': original_repo.created_at.strftime('%Y-%m-%d %H:%M:%S') if original_repo.created_at else 'N/A',
                'fork_created': repo.created_at.strftime('%Y-%m-%d %H:%M:%S') if repo.created_at else 'N/A',
                'forks_count': original_repo.forks_count,
                'open_issues': original_repo.open_issues_count,
            })
    
    # Sort alphabetically by repository name
    return sorted(forks, key=lambda x: x['name'].lower())


def create_csv(forks, username, output_filename='forks_report.csv'):
    """Create a CSV report of forks."""
    
    if not forks:
        print("No forks found!")
        return
    
    # Define CSV headers
    headers = [
        'Repository Name',
        'Your Fork URL',
        'Original Repo URL',
        'Description',
        'Stars (Original)',
        'Language',
        'Original Repo Created',
        'Your Fork Created',
        'Forks Count (Original)',
        'Open Issues (Original)'
    ]
    
    # Write CSV file
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        
        for fork in forks:
            writer.writerow({
                'Repository Name': fork['name'],
                'Your Fork URL': fork['fork_url'],
                'Original Repo URL': fork['original_url'],
                'Description': fork['description'],
                'Stars (Original)': fork['stars'],
                'Language': fork['language'],
                'Original Repo Created': fork['original_created'],
                'Your Fork Created': fork['fork_created'],
                'Forks Count (Original)': fork['forks_count'],
                'Open Issues (Original)': fork['open_issues'],
            })
    
    print(f"✅ CSV generated: {output_filename}")


def main():
    """Main function."""
    import sys
    
    # Configuration
    USERNAME = 'EeveeVictoria'  # Change this to your username
    TOKEN = os.getenv('GITHUB_TOKEN')  # Optional: use personal access token for higher rate limits
    OUTPUT_FILE = 'forks_report.csv'
    
    try:
        # Fetch forks
        forks = get_forks(USERNAME, TOKEN)
        
        if not forks:
            print("No forks found!")
            return
        
        print(f"Found {len(forks)} forks")
        
        # Create CSV
        create_csv(forks, USERNAME, OUTPUT_FILE)
        print(f"\n📄 Report saved to: {OUTPUT_FILE}")
        print(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
