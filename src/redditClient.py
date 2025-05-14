# COSC2671 Social Media and Network Analytics
# @author Jeffrey Chan, RMIT University, 2023
#
import sys
import praw

def redditClient():
    """
    Setup Reddit API authentication.
    Replace username, secrets and passwords with your own.
    @returns: praw Reddit object
    """
    try:
        # fill in with own API information.
        # TODO: you specify with your details
        clientId = ""
        clientSecret = ""
        password = ""
        userName = ""
        userAgents = 'client for SNAM2024'
        
        redditClient = praw.Reddit(
            client_id=clientId,
            client_secret=clientSecret,
            password=password,
            username=userName,
            user_agent=userAgents
        )
        return redditClient
    except Exception as e:
        sys.stderr.write(f"Error occurred: {str(e)}\n")
        sys.exit(1)

# Create the client
client = redditClient()

# Test authentication
try:
    print(client.user.me())
except Exception as e:
    print(f"Authentication failed: {str(e)}")