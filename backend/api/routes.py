from fastapi import APIRouter, UploadFile, File
from services.parser import extract_text_from_pdf
from services.chunker import chunk_text
from services.embedder import generate_embeddings
from services.vectore_store import VectorStore
from services.retreiver import retrieve_chunks
from services.chatbot import chat_with_paper
from services.explainer import explain_section
from services.section_extractor import extract_sections
from services.term_extractor import extract_terms
from services.simplifier import simplify_term
from services.diagram_generator import generate_flow_diagram, generate_analysis_diagram

router = APIRouter()

# GLOBAL STATE (will improve later)
vector_store = None
paper_text = ""
paper_sections = {}
chat_history = []


# UPLOAD PAPER

@router.post("/upload-paper")
async def upload_paper(file: UploadFile = File(...)):
    global vector_store, paper_text, paper_sections

    # Step 1: read file
    contents = await file.read()

    # Step 2: extract text
    text = extract_text_from_pdf(contents)

    # Step 3: NOW assign
    paper_text = text   #  correct position

    # Step 4: extract sections
    paper_sections = extract_sections(text)

    # Step 5: chunking
    chunks = chunk_text(text)

    # Step 6: embeddings
    embeddings = generate_embeddings(chunks)

    # Step 7: vector DB
    vector_store = VectorStore(dimension=embeddings.shape[1])
    vector_store.add(embeddings, chunks)

    return {
        "message": "PDF processed successfully",
        "chunks": len(chunks)
    }


# VECTOR SEARCH
@router.post("/search")
async def search(query: str):
    global vector_store

    if vector_store is None:
        return {"error": "No indexed papers available"}

    results = retrieve_chunks(query, vector_store)

    return {
        "message": "Search completed successfully",
        "relevant_chunks": results
    }


# 💬 CHAT
@router.post("/chat")
async def chat(query: str):
    global vector_store, chat_history

    if vector_store is None:
        return {"error": "No indexed papers available"}

    answer = chat_with_paper(query, vector_store, chat_history)

    chat_history.append({
        "query": query,
        "answer": answer
    })

    return {
        "message": "Chat completed successfully",
        "query": query,
        "answer": answer
    }


#section wise explanation
@router.post("/explain-section")
async def explain_section_endpoint(section_name: str):
    global paper_sections

    if not paper_sections:
        return {"error": "No paper available"}

    content = paper_sections.get(section_name.lower(), "")

    explanation = explain_section(section_name, content)

    return {
        "message": "Section explanation completed successfully",
        "section_name": section_name,
        "explanation": explanation
    }


# TERM SIMPLIFICATION
@router.post("/simplify-terms")
async def simplify_terms():
    global paper_text, vector_store

    if not paper_text or vector_store is None:
        return {"error": "No paper available"}

    terms = extract_terms(paper_text)

    simplified = []

    for term in terms:
        explanation = simplify_term(term, vector_store)

        simplified.append({
            "term": term,
            "meaning": explanation
        })

    return {
        "message": "Terms simplified successfully",
        "terms": simplified
    }


# DIAGRAM GENERATION
@router.post("/generate-diagram")
async def generate_diagram():
    global paper_sections

    if not paper_sections:
        return {
            "error": "No paper available"
        }

    methodology = paper_sections.get("methodology", "")

    if not methodology:
        return {
            "error": "Methodology section not found"
        }

    result = generate_flow_diagram(methodology)

    return {
        "message": "Diagram generated successfully",
        "data": result
    }


#  ANALYSIS REPORT
@router.post("/generate-analysis")
async def generate_analysis():
    global paper_sections

    if not paper_sections:
        return {
            "error": "No paper available"
        }

    result = generate_analysis_diagram(paper_sections)

    return {
        "message": "Analysis generated successfully",
        "data": result
    }