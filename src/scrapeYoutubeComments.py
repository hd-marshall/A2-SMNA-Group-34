import pandas as pd
from youtube_comment_downloader import YoutubeCommentDownloader
import re
from datetime import datetime, timedelta
import csv
import sys
import traceback

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
        # NOTE: The youtube-comment-downloader might not support sort_by parameter
        # Let's try without it first
        try:
            # Try without sort parameter first
            comments_generator = downloader.get_comments_from_url(url)
            
            # Debug: Let's see what the first comment looks like
            print("Getting the first comment for debugging...")
            try:
                first_comment = next(comments_generator)
                print(f"First comment structure: {first_comment.keys()}")
                print(f"Comment likes: {first_comment.get('likes')} (type: {type(first_comment.get('likes'))})")
                
                # Reset the generator
                comments_generator = downloader.get_comments_from_url(url)
            except StopIteration:
                print("No comments found in this video.")
                continue
            except Exception as e:
                print(f"Error getting first comment: {e}")
                traceback.print_exc()
                continue
            
            count = 0
            for comment in comments_generator:
                # Add more debugging
                if count == 0:
                    print(f"Processing comment: {count+1}")
                
                # The error might be here, in the comparison with max_comments
                if count >= int(max_comments):  # Force int conversion
                    print(f"Reached {count} comments for this URL")
                    break
                
                # Extract basic info - with better error handling
                try:
                    text = comment['text']
                    author = comment['author']
                    
                    # Handle likes with extensive debugging
                    likes = 0
                    likes_raw = comment.get('likes', 0)
                    if count == 0:
                        print(f"Raw likes value: {likes_raw} (type: {type(likes_raw)})")
                    
                    if isinstance(likes_raw, str):
                        if 'K' in likes_raw:
                            likes = int(float(likes_raw.replace('K', '')) * 1000)
                        elif 'M' in likes_raw:
                            likes = int(float(likes_raw.replace('M', '')) * 1000000)
                        else:
                            # Try to convert to int, if fails set to 0
                            try:
                                likes = int(likes_raw) if likes_raw.strip() else 0
                            except (ValueError, AttributeError):
                                likes = 0
                    else:
                        # If it's already a number
                        try:
                            likes = int(likes_raw) if likes_raw else 0
                        except (ValueError, TypeError):
                            likes = 0
                    
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
                    if count % 100 == 0:
                        print(f"Processed {count} comments from video {i+1}/{len(url_list)}")
                
                except Exception as e:
                    print(f"Error processing a comment: {e}")
                    traceback.print_exc()
                    continue
            
            print(f"Retrieved {count} comments from {url}")
            
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            print("Full error traceback:")
            traceback.print_exc()
    
    # Check if we have any comments
    if all_comments_list:
        return pd.DataFrame(all_comments_list)
    else:
        print("No comments were collected. Returning empty DataFrame.")
        return pd.DataFrame(columns=['video_id', 'text', 'author', 'likes', 'date', 'time', 'year'])

def save_to_csv(comments_df, filename='youtube_comments.csv'):
    """Save the comments DataFrame to a CSV file"""
    if not comments_df.empty:
        comments_df.to_csv(filename, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8')
        print(f"All comments saved to {filename}")
    else:
        print("No comments to save. CSV file not created.")

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
try:
    comments_df = get_youtube_comments(urls, comments_per_url, sort_by_top=False)  # Try without sorting

    # Only proceed with stats if we have data
    if not comments_df.empty:
        # Display stats
        print("\nComments collected:")
        print(comments_df.groupby('video_id').size())
        
        # Display first few comments to check
        print("\nSample of comments:")
        print(comments_df.head())
        
        # Save all to one CSV
        save_to_csv(comments_df, 'all_youtube_comments.csv')
    else:
        print("No comments were collected. Check your URLs and try again.")
except Exception as e:
    print(f"Critical error in main execution: {e}")
    traceback.print_exc()