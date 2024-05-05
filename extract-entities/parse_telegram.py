import os
import openai
from openai import OpenAI
from string import Template
import json
import glob
from timeit import default_timer as timer
from dotenv import load_dotenv
from time import sleep
from tqdm import tqdm
from typing import List
from node import Node
import csv
# from parser import Parser
from parser_together import Parser
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import islice
import pickle
# Extract information from the given row
def extract_information(row: dict) -> Node:
    result = None
    try:
        result = Parser.extract_events(row["translation"])
        result = result[0] if isinstance(result, list) else None
        result["id"] = row["id"]
        result["time"] = row["time"]
        result["original"] = row["translation"]
    except Exception as e:
        print("Error occurred: ", e)
        print("Dict may be: ", result)
    if result is not None:
        return result
    else:
        return None
    
def process_chunk(chunk, i, file):
    try:
        data = []
        for row in chunk:
            data.append(extract_information(row))

        pickle_file = file + ".pkl"
        with open(pickle_file, "wb") as pf:
            pickle.dump(data, pf)

        with open(file, "w") as f:
            json.dump(data, f)

    except KeyboardInterrupt:
        pickle_file = file + ".pkl"
        with open(pickle_file, "wb") as pf:
            pickle.dump(data, pf)

        with open(file, "w") as f:
            json.dump(data, f)
        print("Data dump completed due to keyboard interrupt.")
        raise
        



def parse_csv(file_path: str) -> None:
    with open(file_path, newline='') as file:
        reader = csv.DictReader(file)
        with ThreadPoolExecutor(max_workers=100) as executor:
            # Split rows into chunks for each worker
            rows = [x for x in reader][:1000]
            n = len(rows) // 100
            row_chunks = [rows[i * n:(i + 1) * n] for i in range(100)]
            row_chunks[-1].extend(rows[16 * n:])  # Include any remaining rows in the last chunk

            # Initialize files for each worker
            files = [f'files/output_worker_{i}.json' for i in range(100)]

            # Submit chunks to the executor and process them
            futures = [executor.submit(process_chunk, chunk, i, files[i]) for i, chunk in enumerate(row_chunks)]

            # Wait for all futures to complete
            for future in tqdm(as_completed(futures), total=len(futures), desc="Processing chunks"):
                future.result()  # We just need to wait for them to complete

            # # Close all files
            # for file in files:
            #     file.close()

    # # Dump all nodes at once at the end
    # with open('empedded_output.json', 'w') as json_file:
    #     json.dump(nodes, json_file)

if __name__ == "__main__":
    path = "../../deftech/russia_social_media.csv"
    parse_csv(path)