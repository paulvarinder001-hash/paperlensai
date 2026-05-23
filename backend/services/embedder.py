from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once (IMPORTANT)
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(chunks):
    """
    Convert text chunks into embeddings
    """
    embeddings = model.encode(chunks)
    
    return np.array(embeddings)