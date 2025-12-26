# type: ignore
import faiss 
import numpy as np

class VectorStore():

    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []
    
    def add_embeddings(self, embeddings: list[list[float]], metadatas: list[dict]):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(metadatas)
        print(self.index)

    def search(self, query_embedding: list[float], k: int = 5):
        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, k)

        results = []
        for idx in indices[0]:
            results.append(self.metadata[idx])
        
        return results