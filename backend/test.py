from agent import Agent
from datetime import datetime

agent = Agent()

context  = [
    "Event details: there are ongoing battles in Terny",
    "Event description: ​🇷🇺⚡️Limansky and Seversky directions, situation at 13:00 March 31, 2024 On the Limansky direction at the turn of Terny - Yampolovka there are oncoming battles. The RF Armed Forces and the Ukrainian Armed Forces are trying to knock each other out of their positions. Units of the Russian Army have not yet managed to build on their success and enter the village of Terny."
]
results = agent.run_search(context, datetime(2024, 3, 30), datetime(2024, 4, 01))
print(results)
