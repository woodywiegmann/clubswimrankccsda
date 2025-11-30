#!/usr/bin/env python3
"""
Twitter posting script for the Cursor pricing tweet.
Requires tweepy library: pip install tweepy

Set your Twitter API credentials as environment variables:
- TWITTER_API_KEY
- TWITTER_API_SECRET
- TWITTER_ACCESS_TOKEN
- TWITTER_ACCESS_TOKEN_SECRET
"""

import os
import sys
import tweepy

def read_tweet():
    """Read the tweet draft from file."""
    try:
        with open('tweet_draft.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: tweet_draft.txt not found")
        sys.exit(1)

def post_tweet():
    """Post the tweet to Twitter."""
    # Get credentials from environment
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("Error: Missing Twitter API credentials")
        print("\nPlease set the following environment variables:")
        print("  export TWITTER_API_KEY='your_api_key'")
        print("  export TWITTER_API_SECRET='your_api_secret'")
        print("  export TWITTER_ACCESS_TOKEN='your_access_token'")
        print("  export TWITTER_ACCESS_TOKEN_SECRET='your_access_token_secret'")
        sys.exit(1)
    
    # Authenticate
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    # Read tweet
    tweet_text = read_tweet()
    
    # Check length (Twitter limit is 280 characters)
    if len(tweet_text) > 280:
        print(f"Warning: Tweet is {len(tweet_text)} characters (limit: 280)")
        print("Twitter will truncate or reject it.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            sys.exit(0)
    
    # Show preview
    print("\n" + "="*60)
    print("TWEET PREVIEW:")
    print("="*60)
    print(tweet_text)
    print("="*60)
    print(f"Length: {len(tweet_text)} characters\n")
    
    # Confirm
    confirm = input("Post this tweet? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Cancelled.")
        sys.exit(0)
    
    # Post tweet
    try:
        api.update_status(tweet_text)
        print("\n✓ Tweet posted successfully!")
    except tweepy.TweepError as e:
        print(f"\n✗ Error posting tweet: {e}")
        sys.exit(1)

if __name__ == '__main__':
    post_tweet()
