from services.chatbot import query_ollama

def explain_section(section_name, content):

    if not content.strip():
        return "Section not found in the paper"

    prompt = f"""
You are an AI assistant that explains research papers.

Explain the following section in simple terms for a beginner.

SECTION: {section_name}

CONTENT:
{content[:1500]}  # limit size

RULES:
- Keep it simple
- Use short sentences
- Do not add external knowledge

EXPLANATION:
"""

    return query_ollama(prompt)