import streamlit as st
import requests
import json
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="PaperLensAI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
BACKEND_URL = "http://localhost:8000"

# Custom styling
st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        font-weight: bold;
        color: #6366f1;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2em;
        color: #6366f1;
        margin-bottom: 1rem;
        border-bottom: 2px solid #6366f1;
        padding-bottom: 0.5rem;
    }
    .upload-box {
        border: 2px dashed #6366f1;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9ff;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'paper_uploaded' not in st.session_state:
    st.session_state.paper_uploaded = False
    st.session_state.chat_history = []

# Sidebar navigation
st.sidebar.markdown("# 📄 PaperLensAI")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📤 Upload Paper", "💬 Chat", "🔍 Search", "📋 Sections", "🏷️ Terms", "📊 Diagrams", "📈 Analysis"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### How it works:
1. Upload a research paper (PDF)
2. Explore its content via chat or search
3. Extract key insights and visualizations
4. Understand terminology and methodology

### Status:
""")

if st.session_state.paper_uploaded:
    st.sidebar.success("✅ Paper loaded and indexed")
else:
    st.sidebar.warning("⚠️ No paper loaded yet")


# PAGE 1: HOME
if page == "🏠 Home":
    st.markdown('<div class="main-header">📄 PaperLensAI</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Smart Research Paper Analyzer</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✨ Features
        
        - **📤 Upload & Process** - Extract text from PDF research papers
        - **💬 Chat Interface** - Ask questions about your paper (RAG-based)
        - **🔍 Semantic Search** - Find relevant information using embeddings
        - **📋 Section Extract** - Explainable summaries of each section
        - **🏷️ Term Simplification** - Understand complex terminology
        - **📊 Diagrams** - Visualize methodology flowcharts
        - **📈 Analysis** - Get comprehensive paper analysis metrics
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Quick Start
        
        1. Click "📤 Upload Paper" to load a PDF
        2. Wait for processing (this may take a minute)
        3. Navigate through different analysis options
        4. Ask questions, search, or explore sections
        
        ### 🛠️ Tech Stack
        
        - **Frontend**: Streamlit
        - **Backend**: FastAPI + LLM (Ollama)
        - **Embeddings**: Sentence Transformers
        - **Vector DB**: NumPy FAISS
        - **PDF Processing**: PyPDF / Fitz
        """)
    
    st.markdown("---")
    st.markdown("""
    ### 📊 About This Tool
    
    PaperLensAI leverages advanced NLP and Machine Learning to transform complex research papers 
    into actionable insights. Whether you're a researcher, student, or professional, this tool 
    helps you understand papers faster and extract key information efficiently.
    """)


# PAGE 2: UPLOAD PAPER
elif page == "📤 Upload Paper":
    st.markdown('<h2 class="section-header">Upload Research Paper</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Upload a research paper in PDF format. The system will:
        - Extract text and structure
        - Split into chunks
        - Generate embeddings
        - Index for search and retrieval
        """)
        
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None:
            col_upload, col_preview = st.columns([1, 1])
            
            with col_upload:
                if st.button("📤 Process Paper", use_container_width=True, type="primary"):
                    with st.spinner("Processing paper... This may take a minute"):
                        try:
                            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                            response = requests.post(
                                f"{BACKEND_URL}/upload-paper",
                                files=files,
                                timeout=120
                            )
                            
                            if response.status_code == 200:
                                data = response.json()
                                st.session_state.paper_uploaded = True
                                st.session_state.chat_history = []
                                
                                st.markdown(f"""
                                <div class="success-box">
                                ✅ Success! Paper processed successfully<br>
                                📊 Total chunks: {data.get('chunks', 'N/A')}
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div class="error-box">
                                ❌ Error: {response.json().get('error', 'Unknown error')}
                                </div>
                                """, unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f"""
                            <div class="error-box">
                            ❌ Error: {str(e)}<br>
                            Make sure the backend is running at {BACKEND_URL}
                            </div>
                            """, unsafe_allow_html=True)
            
            with col_preview:
                st.info(f"📄 {uploaded_file.name}\n\nSize: {uploaded_file.size / 1024:.1f} KB")
    
    with col2:
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Use a clear, well-formatted PDF
        - Academic papers work best
        - Typical processing time: 30-60 seconds
        - PDF should be text-based (not scanned images)
        """)


# PAGE 3: CHAT
elif page == "💬 Chat":
    st.markdown('<h2 class="section-header">Chat with Your Paper</h2>', unsafe_allow_html=True)
    
    if not st.session_state.paper_uploaded:
        st.warning("⚠️ Please upload a paper first from the 📤 Upload Paper section")
    else:
        st.markdown("""
        Ask questions about the paper. The system uses Retrieval-Augmented Generation (RAG) 
        to provide accurate, context-aware answers based on the paper's content.
        """)
        
        # Display chat history
        chat_container = st.container()
        
        with chat_container:
            for i, msg in enumerate(st.session_state.chat_history):
                with st.chat_message("user"):
                    st.markdown(msg["query"])
                with st.chat_message("assistant"):
                    st.markdown(msg["answer"])
        
        # Chat input
        col_input, col_send = st.columns([5, 1]
        )
        
        with col_input:
            user_question = st.text_input(
                "Ask a question about the paper...",
                placeholder="e.g., What is the main contribution of this paper?",
                key="chat_input"
            )
        
        with col_send:
            if st.button("Send", use_container_width=True, type="primary", key="send_btn"):
                if user_question:
                    with st.spinner("Thinking..."):
                        try:
                            response = requests.post(
                                f"{BACKEND_URL}/chat",
                                params={"query": user_question},
                                timeout=300
                            )
                            
                            if response.status_code == 200:
                                data = response.json()
                                st.session_state.chat_history.append({
                                    "query": user_question,
                                    "answer": data.get("answer", "No answer generated")
                                })
                                st.rerun()
                            else:
                                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")


# PAGE 4: SEARCH
elif page == "🔍 Search":
    st.markdown('<h2 class="section-header">Semantic Search</h2>', unsafe_allow_html=True)
    
    if not st.session_state.paper_uploaded:
        st.warning("⚠️ Please upload a paper first from the 📤 Upload Paper section")
    else:
        st.markdown("""
        Search for relevant sections in your paper using natural language. 
        The system finds semantically similar content using embeddings.
        """)
        
        search_query = st.text_input(
            "Search query",
            placeholder="e.g., machine learning algorithms, data preprocessing...",
            key="search_input"
        )
        
        col_search, col_num = st.columns([3, 1])
        
        with col_search:
            if st.button("🔍 Search", use_container_width=True, type="primary"):
                if search_query:
                    with st.spinner("Searching..."):
                        try:
                            response = requests.post(
                                f"{BACKEND_URL}/search",
                                params={"query": search_query},
                                timeout=300
                            )
                            
                            if response.status_code == 200:
                                data = response.json()
                                results = data.get("relevant_chunks", [])
                                
                                st.markdown("### 📋 Results")
                                
                                if results:
                                    for i, chunk in enumerate(results, 1):
                                        with st.expander(f"📄 Result {i}"):
                                            st.markdown(chunk)
                                else:
                                    st.info("No results found for this query")
                            else:
                                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        
        with col_num:
            st.info("🔎 Semantic matching")


# PAGE 5: SECTIONS
elif page == "📋 Sections":
    st.markdown('<h2 class="section-header">Section Analysis</h2>', unsafe_allow_html=True)
    
    if not st.session_state.paper_uploaded:
        st.warning("⚠️ Please upload a paper first from the 📤 Upload Paper section")
    else:
        st.markdown("""
        Get detailed explanations of specific sections in the paper. 
        Choose a section to understand its content better.
        """)
        
        # Common section names
        sections = [
            "Abstract",
            "Introduction",
            "Literature Review",
            "Methodology",
            "Results",
            "Discussion",
            "Conclusion",
            "References"
        ]
        
        col_section, col_custom = st.columns([1, 1])
        
        with col_section:
            selected_section = st.selectbox("Select a section:", sections)
        
        with col_custom:
            custom_section = st.text_input("Or enter custom section name:", "")
        
        section_to_analyze = custom_section if custom_section else selected_section
        
        if st.button("📊 Analyze Section", use_container_width=True, type="primary"):
            with st.spinner("Analyzing section..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/explain-section",
                        params={"section_name": section_to_analyze},
                        timeout=300
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        st.markdown(f"### 📖 {data.get('section_name', section_to_analyze)}")
                        st.markdown("---")
                        st.markdown(data.get("explanation", "No explanation available"))
                    else:
                        error_msg = response.json().get('error', 'Section not found')
                        st.warning(f"⚠️ {error_msg}\n\nTry one of these sections: {', '.join(sections)}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# PAGE 6: TERMS
elif page == "🏷️ Terms":
    st.markdown('<h2 class="section-header">Term Simplification</h2>', unsafe_allow_html=True)
    
    if not st.session_state.paper_uploaded:
        st.warning("⚠️ Please upload a paper first from the 📤 Upload Paper section")
    else:
        st.markdown("""
        Extract and simplify complex terminology from your paper. 
        Get plain-language explanations of technical terms.
        """)
        
        if st.button("🔬 Extract & Simplify Terms", use_container_width=True, type="primary"):
            with st.spinner("Extracting and simplifying terms..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/simplify-terms",
                        timeout=300
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        terms = data.get("terms", [])
                        
                        st.markdown(f"### 📚 Simplified Terms ({len(terms)} found)")
                        st.markdown("---")
                        
                        if terms:
                            for term_data in terms:
                                term = term_data.get("term", "Unknown")
                                meaning = term_data.get("meaning", "No explanation available")
                                
                                with st.expander(f"**{term}**"):
                                    st.markdown(meaning)
                        else:
                            st.info("No terms found")
                    else:
                        st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# PAGE 7: DIAGRAMS
elif page == "📊 Diagrams":
    st.markdown('<h2 class="section-header">Methodology Diagram</h2>', unsafe_allow_html=True)
    
    if not st.session_state.paper_uploaded:
        st.warning("⚠️ Please upload a paper first from the 📤 Upload Paper section")
    else:
        st.markdown("""
        Generate a visual flowchart of the paper's methodology using Excalidraw. 
        Get a clear visualization of the research approach.
        """)
        
        if st.button("📐 Generate Methodology Diagram", use_container_width=True, type="primary"):
            with st.spinner("Generating diagram..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/generate-diagram",
                        timeout=300
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        diagram_data = data.get("data", {})
                        
                        st.success("✅ Diagram generated successfully!")
                        
                        # Display as JSON or embed
                        with st.expander("📋 Diagram Data (Excalidraw JSON)"):
                            st.json(diagram_data)
                        
                        st.info("""
                        💡 You can copy this JSON and paste it into Excalidraw.com 
                        to view and edit the diagram interactively.
                        """)
                    else:
                        st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# PAGE 8: ANALYSIS
elif page == "📈 Analysis":
    st.markdown('<h2 class="section-header">Paper Analysis Report</h2>', unsafe_allow_html=True)
    
    if not st.session_state.paper_uploaded:
        st.warning("⚠️ Please upload a paper first from the 📤 Upload Paper section")
    else:
        st.markdown("""
        Generate a comprehensive analysis report of your paper including metrics, 
        key findings, and research classification.
        """)
        
        if st.button("📊 Generate Analysis Report", use_container_width=True, type="primary"):
            with st.spinner("Generating analysis report..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/generate-analysis",
                        timeout=300
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        analysis_data = data.get("data", {})
                        
                        st.success("✅ Analysis report generated successfully!")
                        
                        # Display metrics if available
                        if "metrics" in analysis_data:
                            st.markdown("### 📊 Key Metrics")
                            
                            col1, col2, col3, col4 = st.columns(4)
                            
                            metrics = analysis_data.get("metrics", {})
                            
                            with col1:
                                st.metric("Complexity", metrics.get("complexity", "N/A"))
                            with col2:
                                st.metric("Novelty", metrics.get("novelty", "N/A"))
                            with col3:
                                st.metric("Significance", metrics.get("significance", "N/A"))
                            with col4:
                                st.metric("Clarity", metrics.get("clarity", "N/A"))
                        
                        # Display report sections
                        if "report" in analysis_data:
                            report = analysis_data.get("report", {})
                            
                            st.markdown("### 📝 Analysis Report")
                            
                            for section, content in report.items():
                                with st.expander(f"📌 {section.title()}"):
                                    st.markdown(content)
                        
                        # Display full data if needed
                        with st.expander("📋 Full Analysis Data (JSON)"):
                            st.json(analysis_data)
                    else:
                        st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")


