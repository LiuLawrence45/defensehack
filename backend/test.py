from agent import Agent

agent = Agent()

context  = [
    "Event details:",
    "Event description: "
]
results = agent.run_search(context, datetime(2024, 3, 30), datetime(2024, 4, 01))
print(results)
