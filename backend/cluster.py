import pickle
from sklearn.metrics.pairwise import cosine_similarity
import json

class Cluster:

    def __init__(self) -> None:
        with open('embeds.pkl', 'rb') as file:
            self.embeddings = pickle.load(file)

        with open("data.json", "r") as file:
            self.og_data = json.load(file)
            
    
    def embed(self):
        self.sim =  cosine_similarity(self.embeddings)

    def cluster(self, threshold):
        clustered = {}
        used_js = set()
        for i, row in enumerate(self.sim):
            clustered[i] = []
            for j, value in enumerate(row):
                if value > threshold and i != j and i not in used_js:
                    clustered[i].append(j)
                    used_js.add(j)
        
        self.cluster = clustered
    
    def get_clusters(self):
        text_data = self.og_data
        list_of_entries = []
        for index, similar_indices in self.clustered.items():
            data = []
            if len(similar_indices) > 1:
                data.append(text_data[index])
                for similar_index in similar_indices:
                    data.append(text_data[similar_index])
        
        return list_of_entries



# info = cosine_similarity(embeddings[:30000])

    
