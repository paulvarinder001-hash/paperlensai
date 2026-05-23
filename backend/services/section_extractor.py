import re

def extract_sections(text):
    """
    Extract common research paper sections
    """

    sections = {
        "abstract": "",
        "introduction": "",
        "methodology": "",
        "results": "",
        "conclusion": ""
    }

    # Normalize text
    text = text.lower()

    # Simple regex patterns using non-capturing groups
    patterns = {
        "abstract": r"(?:abstract)(.*?)(?:introduction|methodology|methods|background)",
        "introduction": r"(?:introduction)(.*?)(?:methodology|methods|approach|related work)",
        "methodology": r"(?:methodology|methods|approach)(.*?)(?:results|experiments|evaluation)",
        "results": r"(?:results|experiments|evaluation)(.*?)(?:conclusion|discussion)",
        "conclusion": r"(?:conclusion|discussion)(.*)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            # group(1) is now guaranteed to be the (.*?) content
            sections[key] = match.group(1).strip()

    return sections