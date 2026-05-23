from services.chatbot import query_ollama
from services.retreiver import retrieve_chunks

def simplify_term(term, vector_store):

    chunks = retrieve_chunks(term, vector_store, top_k=2)

    context = "\n".join(chunks)

    prompt = f"""
Explain this term using the given context.

TERM: {term}

CONTEXT:
{context}

RULES:
- Simple explanation
- 2-3 lines only

ANSWER:
"""

    return query_ollama(prompt)