from agent import Agent
from datetime import datetime

agent = Agent()

context  = [
    "Event details: Destruction of Radar and S-300 Launcher near Zmiev",
    "Event descriptionL: The 40V6M universal tower with the 30N6 illumination and guidance radar, as well as the S-300PS air defense missile launcher of the Ukrainian army near the city of Zmiev in the Kharkov region, were destroyed. The footage captured the impact of an air-detonated missile on the tower and the subsequent detonation of solid fuel in the missile launcher"
    # "Event details: An assault group of fagots was destroyed in the village of #Pervomaiskoye, through the lens of the operator of the 11th separate motorized infantry battalion “Kievan Rus”🔥💥💪🇺🇦",
    # # "Event description: ​🇷🇺⚡️Limansky and Seversky directions, situation at 13:00 March 31, 2024 On the Limansky direction at the turn of Terny - Yampolovka there are oncoming battles. The RF Armed Forces and the Ukrainian Armed Forces are trying to knock each other out of their positions. Units of the Russian Army have not yet managed to build on their success and enter the village of Terny."
]
results = agent.run_search(context, datetime(2024, 3, 30), datetime(2024, 4, 1))
# Convert the dictionary of relevant tweets into a list
relevant_tweets_list = [tweet for tweets in results.values() for tweet in tweets]
# Use the agent's summarize method to generate a summary
summary = agent.summarize(context, relevant_tweets_list)

# for tweet in relevant_tweets_list:
#     print(tweet.text)


print("Summary of the event based on the relevant tweets:")

print(summary)




# from twitter_q import TwitterSearchClient

# # Initialize the TwitterSearchClient
# twitter_client = TwitterSearchClient()

# # Define the tweet IDs to fetch
# tweet_ids = {
#     'DPR Ukraine': ["1774512865925534197", "1774509662676677098", "1774425824998854689", "1774341098468430229"],
#     'Ukraine shelling': ["1774512865925534197", "1774509662676677098"],
#     'Donetsk shelling': ["1774460116278133247", "1774425824998854689", "1774424241716285736"]
# }
# # Fetch and print the text of each tweet
# for location, ids in tweet_ids.items():
#     for tweet_id in ids:
#         tweet = twitter_client.get_tweet_by_id(tweet_id)
#         if tweet:
#             print(f"{tweet.text.replace('\n', '')} - {tweet.created_at}\n\n")



