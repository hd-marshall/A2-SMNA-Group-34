import pandas as pd
from youtube_comment_downloader import YoutubeCommentDownloader
import re
from datetime import datetime, timedelta
import csv

# Initialize the downloader
downloader = YoutubeCommentDownloader()

def get_youtube_comments(url_list, comments_per_url, sort_by_top=True):
    # Get system time - using your OS time
    current_date = datetime.now()
    print(f"Current system time (from your OS): {current_date}")
    
    all_comments_list = []
    
    # Process each URL
    for i, (url, max_comments) in enumerate(zip(url_list, comments_per_url)):
        print(f"Processing URL {i+1}/{len(url_list)}: {url} - Getting {max_comments} comments")
        
        # Set sort option if requested
        sort = "top" if sort_by_top else None
        
        # Get comments
        try:
            comments = downloader.get_comments_from_url(url, sort_by=sort)
            
            count = 0
            for comment in comments:
                if count >= max_comments:
                    break
                    
                # Extract basic info
                text = comment['text']
                author = comment['author']
                likes = comment.get('likes', 0)
                time_ago = comment.get('time', '')
                
                # Parse the "time ago" text to estimate a date
                estimated_date = current_date
                
                # Extract time information using regex
                time_match = re.search(r'(\d+)\s+(second|minute|hour|day|week|month|year)s?\s+ago', time_ago)
                
                if time_match:
                    value = int(time_match.group(1))
                    unit = time_match.group(2)
                    
                    # Adjust the current date based on the time ago
                    if unit == 'year':
                        estimated_date = current_date.replace(year=current_date.year - value)
                    elif unit == 'month':
                        month = current_date.month - value
                        year = current_date.year
                        while month <= 0:
                            month += 12
                            year -= 1
                        estimated_date = current_date.replace(year=year, month=month)
                    elif unit == 'week':
                        estimated_date = current_date - timedelta(days=value * 7)
                    elif unit == 'day':
                        estimated_date = current_date - timedelta(days=value)
                    elif unit == 'hour':
                        estimated_date = current_date - timedelta(hours=value)
                    elif unit == 'minute':
                        estimated_date = current_date - timedelta(minutes=value)
                    elif unit == 'second':
                        estimated_date = current_date - timedelta(seconds=value)
                
                # Round to nearest hour
                minutes = estimated_date.minute
                if minutes >= 30:
                    # Round up to the next hour
                    estimated_date = estimated_date.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                else:
                    # Round down to the current hour
                    estimated_date = estimated_date.replace(minute=0, second=0, microsecond=0)
                
                # Format date and time
                date_str = estimated_date.strftime('%Y-%m-%d')
                time_str = estimated_date.strftime('%H:%M:%S')
                year = estimated_date.year
                
                # Extract video ID from URL
                video_id = url.split('v=')[1].split('&')[0] if 'v=' in url else url.split('/')[-1]
                
                all_comments_list.append({
                    'video_id': video_id,
                    'text': text,
                    'author': author,
                    'likes': likes,
                    'date': date_str,
                    'time': time_str,
                    'year': year
                })
                
                count += 1
                
            print(f"Retrieved {count} comments from {url}")
            
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
    
    return pd.DataFrame(all_comments_list)

def save_to_csv(comments_df, filename='youtube_comments.csv'):
    """Save the comments DataFrame to a CSV file"""
    comments_df.to_csv(filename, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8')
    print(f"All comments saved to {filename}")

# Example usage - define your URLs and comment counts
urls = [
    # 2025 - Part 1 - HauteLeMode
    'https://www.youtube.com/watch?v=iWS3oVeyjL4',
    # 2025 - Part 2 - HauteLeMode
    'https://www.youtube.com/watch?v=Ar9NFhmSnrk',
    # 2024 - HauteLeMode
    'https://www.youtube.com/watch?v=P71sr0kZY7o',
    # 2023 - Part 1 - HauteLeMode
    'https://www.youtube.com/watch?v=E_WcvAiKQfI',
    # 2023 - Part 2 - HauteLeMode
    'https://www.youtube.com/watch?v=XUIB4oWw37I',
    # 2022 - HauteLeMode
    'https://www.youtube.com/watch?v=PbRZcvVnF0w',
    # 2021 - HauteLeMode
    'https://www.youtube.com/watch?v=ZMrgtotgThk'
]

# Number of comments to retrieve for each URL
comments_per_url = [1500, 1500, 3000, 1500, 500, 2000, 2000]

# Get comments with date and time
comments_df = get_youtube_comments(urls, comments_per_url, sort_by_top=True)

# Display stats
print("\nComments collected:")
print(comments_df.groupby('video_id').size())

# Display first few comments to check
print("\nSample of comments:")
print(comments_df.head())

# Save all to one CSV
save_to_csv(comments_df, 'all_youtube_comments.csv')