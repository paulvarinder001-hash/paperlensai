import requests
from services.retreiver import retrieve_chunks

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen:0.5b"

def query_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

def rerank_chunks(query, chunks):
    # simple scoring based on keyword overlap
    scored = []

    for chunk in chunks:
        score = sum(1 for word in query.lower().split() if word in chunk.lower())
        scored.append((score, chunk))

    # sort by score descending
    scored.sort(reverse=True)

    # return top 3
    return [chunk for _, chunk in scored[:3]]

def build_prompt(context_chunks, user_query,chat_history):
    context = "\n\n".join(context_chunks)

    history_text = ""

    for chat in chat_history[-3:]:
        history_text += f"""User: {chat['query']}\nAssistant: {chat['answer']}\n"""

    prompt = f"""
You are a research paper assistant.

STRICT RULES:
- Answer ONLY from CONTEXT
- Do NOT use prior knowledge
- If unsure → say "Not found in the paper"
- Be concise and clear
- Avoid assumptions

CHAT HISTORY:
{history_text}

CONTEXT:
{context}

QUESTION:
{user_query}

FINAL ANSWER:
"""

    return prompt

def chat_with_paper(user_query, vector_store,chat_history):
    # retrieve relevant chunks based on user query
    relevant_chunks = retrieve_chunks(user_query, vector_store,top_k=3)

    # retreive the best chunks based on simple keyword overlap scoring
    best_chunks = rerank_chunks(user_query, relevant_chunks)

    # build prompt for the language model
    prompt = build_prompt(best_chunks, user_query,chat_history)

    # get response from Ollama
    answer = query_ollama(prompt)

    return answer