    # def search_telegram(self, search_field="description", search_query="", start_time=None, end_time=None) -> List(Document):
    #     collection = self.client["telegram"]["data"]

    #     # Create index for the search field and time
    #     collection.create_index([(search_field, 1), ("time", 1)])

    #     # Query is a dict, with the keys = to fields in each object in MongoDB
    #     query = {}

    #     # If a search query is provided, add as a key.
    #     if search_query:
    #         query[search_field] = search_query

    #     # # If time range is not provided, default to the past two weeks
    #     if not start_time or not end_time:
    #         end_time = datetime.now()
    #         start_time = end_time - timedelta(weeks=2)


    #     query["time"] = {"$gte": start_time, "$lte": end_time}

    #     print("Query is: ", query)

    #     try:
    #         results = collection.find(query)
    #         for result in results:
    #             print(result["time"])
    #         return list(results)
        
    #     except Exception as e:
    #         print("Error occurred: ", e)
