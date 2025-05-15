import pandas as pd
from youtube_comment_downloader import YoutubeCommentDownloader
import re
from datetime import datetime, timedelta
import csv
import sys
import traceback

# ============= CONFIGURATION SECTION =============
# This section contains all the URLs and their corresponding years
# Add new URLs and years here

# URL Configuration - Dictionary with URL as key and Met Gala year as value
URL_CONFIG = {
    # 2025 Videos
    'https://www.youtube.com/watch?v=iWS3oVeyjL4': 2025,  # 2025 - Part 1 - HauteLeMode
    'https://www.youtube.com/watch?v=Ar9NFhmSnrk': 2025,  # 2025 - Part 2 - HauteLeMode
    'https://www.youtube.com/watch?v=YMPPo7APaoA': 2025,  # 2025 - Part 3 - HauteLeMode
    'https://www.youtube.com/watch?v=NW2oiPiqByk': 2025,  # Vogue Met Gala Live 2025
    'https://www.youtube.com/watch?v=AyFzKATCiv0': 2025,  # Vogue Lisa
    'https://www.youtube.com/watch?v=BbAgK_jGRfE': 2025,  # Chris Klemmins 2025
    
    # 2024 Videos
    'https://www.youtube.com/watch?v=P71sr0kZY7o': 2024,  # 2024 - HauteLeMode
    'https://www.youtube.com/watch?v=JGVq7J5_sTk': 2024,  # Vogue Met Gala Live 2024
    'https://www.youtube.com/watch?v=jlR-T42I18E': 2024,  # Vogue Kendall Jenner
    'https://www.youtube.com/watch?v=urdBX1l0I6I': 2024,  # Chris Klemmins 2024
    'https://www.youtube.com/watch?v=RqYRTmpBu0k&t=3s': 2024, # Rent free 2024
    
    # 2023 Videos
    'https://www.youtube.com/watch?v=E_WcvAiKQfI': 2023,  # 2023 - Part 1 - HauteLeMode
    'https://www.youtube.com/watch?v=XUIB4oWw37I': 2023,  # 2023 - Part 2 - HauteLeMode
    'https://www.youtube.com/watch?v=LHCTW4pckDo': 2023,   # Vogue Met Gala Live 2023
    "https://www.youtube.com/watch?v=LHCTW4pckDo&t=122s": 2023,  # Vogue Met Gala
    
    # 2022 Videos
    'https://www.youtube.com/watch?v=PbRZcvVnF0w': 2022,  # 2022 - HauteLeMode
    'https://www.youtube.com/watch?v=ItZ4SlxpOiI': 2022,  # 2022 Met Gala Vogue
    'https://www.youtube.com/watch?v=lyJqXb8Nj-I': 2022,  # Harpers Bazaar - 2022
    'https://www.youtube.com/watch?v=cpFc1RPOF7s': 2022,  # Jack Harlow
    
    # 2021 Videos
    'https://www.youtube.com/watch?v=ZMrgtotgThk': 2021,  # 2021 - HauteLeMode
    'https://www.youtube.com/watch?v=mrFfGptVzrI': 2021,   # 2021 - Met Gala - Vanity Fair
    'https://www.youtube.com/watch?v=qEvQa6xayYE': 2021,    # Additional 2021 video
    'https://www.youtube.com/watch?v=qKYhgn1TiV4&t=11s': 2021  # Another 2021 video
    
    # Add new URLs here in the same format:
    # 'https://www.youtube.com/watch?v=VIDEO_ID': YEAR,
}

# Output file configuration
OUTPUT_FILE = 'all_youtube_comments.csv'

# Progress report interval (print status every X comments)
PROGRESS_INTERVAL = 100

# Sort comments by top (set to False for chronological)
SORT_BY_TOP = False

# Maximum processing time per video in seconds (0 for unlimited)
# Set this to a value (e.g., 3600 for 1 hour) if you want to limit processing time per video
MAX_TIME_PER_VIDEO = 0  # 0 means unlimited

# ============= END CONFIGURATION SECTION =============

# Initialize the downloader
downloader = YoutubeCommentDownloader()

def get_youtube_comments(url_config, sort_by_top=True, max_time_per_video=0):
    """
    Retrieve ALL available YouTube comments for multiple videos
    
    Args:
        url_config: Dictionary with URLs as keys and Met Gala years as values
        sort_by_top: Whether to sort comments by popularity
        max_time_per_video: Maximum time to spend per video in seconds (0 = unlimited)
    
    Returns:
        DataFrame containing all collected comments
    """
    # Get system time - using your OS time
    current_date = datetime.now()
    print(f"Current system time (from your OS): {current_date}")
    
    all_comments_list = []
    
    # Process each URL
    total_urls = len(url_config)
    for i, (url, met_gala_year) in enumerate(url_config.items()):
        print(f"\nProcessing URL {i+1}/{total_urls}: {url}")
        print(f"Getting ALL available comments for Met Gala {met_gala_year}")
        
        try:
            # Track start time for this video
            start_time = datetime.now()
            
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
                # Check if we've exceeded the time limit for this video
                if max_time_per_video > 0:
                    elapsed_time = (datetime.now() - start_time).total_seconds()
                    if elapsed_time > max_time_per_video:
                        print(f"Time limit ({max_time_per_video} seconds) reached for this video. Moving to next.")
                        break
                
                # Add debugging for first comment
                if count == 0:
                    print(f"Processing comment: {count+1}")
                
                # Extract basic info - with better error handling
                try:
                    # Get the text and replace newlines with spaces to keep all text on one line
                    text = comment['text'].replace('\n', ' ').replace('\r', ' ')
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
                        'year': year,
                        'met_gala_year': met_gala_year  # Add the Met Gala year
                    })
                    
                    count += 1
                    if count % PROGRESS_INTERVAL == 0:
                        elapsed_min = (datetime.now() - start_time).total_seconds() / 60
                        rate = count / elapsed_min if elapsed_min > 0 else 0
                        print(f"Processed {count} comments from video {i+1}/{total_urls} ({elapsed_min:.1f} minutes, {rate:.1f} comments/min)")
                
                except Exception as e:
                    print(f"Error processing a comment: {e}")
                    traceback.print_exc()
                    continue
            
            # Calculate and display stats for this video
            elapsed_time = (datetime.now() - start_time).total_seconds()
            minutes = elapsed_time / 60
            rate = count / minutes if minutes > 0 else 0
            
            print(f"\nRetrieved {count} comments from {url}")
            print(f"Time taken: {minutes:.1f} minutes ({rate:.1f} comments/minute)")
            
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            print("Full error traceback:")
            traceback.print_exc()
    
    # Check if we have any comments
    if all_comments_list:
        return pd.DataFrame(all_comments_list)
    else:
        print("No comments were collected. Returning empty DataFrame.")
        return pd.DataFrame(columns=['video_id', 'text', 'author', 'likes', 'date', 'time', 'year', 'met_gala_year'])

def save_to_csv(comments_df, filename='youtube_comments.csv'):
    """Save the comments DataFrame to a single CSV file without backups"""
    if not comments_df.empty:
        # Use lineterminator parameter to ensure proper line handling
        comments_df.to_csv(filename, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8', lineterminator='\n')
        print(f"All comments saved to {filename}")
    else:
        print("No comments to save. CSV file not created.")

def display_stats(comments_df):
    """Display statistics about the collected comments"""
    if comments_df.empty:
        print("No comments to analyze.")
        return
        
    # Display stats
    print("\nComments collected by video:")
    video_counts = comments_df.groupby('video_id').size()
    print(video_counts)
    print(f"Total videos: {len(video_counts)}")
    
    # Display stats by Met Gala year
    print("\nComments by Met Gala Year:")
    year_counts = comments_df.groupby('met_gala_year').size()
    print(year_counts)
    
    # Display total counts
    total_comments = len(comments_df)
    print(f"\nTotal comments collected: {total_comments}")
    
    # Display comments by posted year vs Met Gala year
    print("\nComments by Posted Year vs Met Gala Year:")
    year_comparison = pd.crosstab(comments_df['year'], comments_df['met_gala_year'])
    print(year_comparison)
    
    # Display first few comments to check
    print("\nSample of comments:")
    print(comments_df.head())
    
    # Display distribution of likes
    print("\nLikes statistics:")
    likes_stats = comments_df['likes'].describe()
    print(likes_stats)
    
    # Find most liked comments
    print("\nTop 5 most liked comments:")
    top_comments = comments_df.sort_values('likes', ascending=False).head(5)
    for i, (_, comment) in enumerate(top_comments.iterrows()):
        print(f"{i+1}. {comment['likes']} likes - {comment['text'][:100]}...")

def main():
    """Main function to run the comment collection process"""
    try:
        # Display script start info
        print("=" * 60)
        print("YouTube Comment Collector - UNLIMITED MODE")
        print("This script will attempt to collect ALL available comments")
        print("Press Ctrl+C at any time to stop and save collected comments")
        print("=" * 60)
        
        start_time = datetime.now()
        print(f"Script started at: {start_time}")
        
        try:
            # Get comments - passing the time limit parameter
            comments_df = get_youtube_comments(
                URL_CONFIG, 
                sort_by_top=SORT_BY_TOP,
                max_time_per_video=MAX_TIME_PER_VIDEO
            )
            
            # Display statistics
            display_stats(comments_df)
            
            # Save to CSV - only one file
            save_to_csv(comments_df, OUTPUT_FILE)
            
        except KeyboardInterrupt:
            print("\n\nScript interrupted by user!")
            print("Saving collected comments so far...")
            
            # Save only one file even on interruption
            if 'all_comments_list' in locals() and all_comments_list:
                partial_df = pd.DataFrame(all_comments_list)
                save_to_csv(partial_df, OUTPUT_FILE)  # Save to the main output file
                display_stats(partial_df)
            else:
                print("No comments collected yet.")
        
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds() / 60.0
        print(f"\nScript finished at: {end_time}")
        print(f"Total run time: {elapsed_time:.1f} minutes")
        
    except Exception as e:
        print(f"Critical error in main execution: {e}")
        traceback.print_exc()

# Run the program if called directly
if __name__ == "__main__":
    main()
