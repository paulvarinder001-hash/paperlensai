from services.simple_excalidraw import (
    generate_simple_flow,
    generate_simple_analysis
)


def generate_flow_diagram(methodology_text):
    """Generate Excalidraw flowchart from methodology"""
    try:
        excalidraw_data = generate_simple_flow(methodology_text)
        
        if not excalidraw_data or not excalidraw_data.get("elements"):
            return {"error": "Could not generate diagram"}
        
        return {
            "excalidraw": excalidraw_data,
            "type": "flowchart"
        }
    except Exception as e:
        print(f"Diagram generation error: {e}")
        return {"error": f"Failed to generate diagram: {str(e)}"}


def generate_analysis_diagram(paper_sections):
    """Generate analysis dashboard from paper sections"""
    try:
        result = generate_simple_analysis(paper_sections)
        
        if not result or not result.get("elements"):
            return {"error": "Could not generate analysis"}
        
        return {
            "excalidraw": result,
            "report": result.get("report", {}),
            "type": "analysis"
        }
    except Exception as e:
        print(f"Analysis generation error: {e}")
        return {"error": f"Failed to generate analysis: {str(e)}"}