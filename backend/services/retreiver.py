from services.embedder import model
import numpy as np


def retrieve_chunks(query, vector_store, top_k=5):

    query=f"Explain clearly in simple terms: {query}"
    """
    Convert query → embedding → retrieve similar chunks
    """
    query_embedding = model.encode([query])
    
    results = vector_store.search(query_embedding, top_k=top_k)
    
    return results