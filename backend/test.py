from agent import Agent
from datetime import datetime

# agent = Agent()

# context  = [
#     "Event details: ⚡️Over the past 24 hours, Ukrainian armed forces have shelled residential areas of the DPR",
#     # "Event description: ​🇷🇺⚡️Limansky and Seversky directions, situation at 13:00 March 31, 2024 On the Limansky direction at the turn of Terny - Yampolovka there are oncoming battles. The RF Armed Forces and the Ukrainian Armed Forces are trying to knock each other out of their positions. Units of the Russian Army have not yet managed to build on their success and enter the village of Terny."
# ]
# results = agent.run_search(context, datetime(2024, 3, 30), datetime(2024, 4, 1))
# print(results)

from twitter_q import TwitterSearchClient

# Initialize the TwitterSearchClient
twitter_client = TwitterSearchClient()

# Define the tweet IDs to fetch
tweet_ids = {
    'DPR Ukraine': ["1774512865925534197", "1774509662676677098", "1774425824998854689", "1774341098468430229"],
    'Ukraine shelling': ["1774512865925534197", "1774509662676677098"],
    'Donetsk shelling': ["1774460116278133247", "1774425824998854689", "1774424241716285736"]
}
# Fetch and print the text of each tweet
for location, ids in tweet_ids.items():
    for tweet_id in ids:
        tweet = twitter_client.get_tweet_by_id(tweet_id)
        if tweet:
            print(tweet.text.replace('\n', '') + "\n\n")
