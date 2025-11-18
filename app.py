"""
Multi-Language Code Analyzer with AST Visualization
A Streamlit application for parsing and visualizing Abstract Syntax Trees
"""

import streamlit as st
import traceback
from parser_utils import (
    parse_code,
    ast_to_graphviz,
    get_ast_summary,
    SUPPORTED_LANGUAGES,
    initialize_parsers
)

# Optional LLM integration
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def analyze_with_llm(code: str, language: str, ast_summary: str) -> str:
    """
    Send code and AST summary to LLM for analysis using Gemini 2.5 Flash
    """
    if not GEMINI_AVAILABLE:
        return "Google Generative AI library not available. Install with: pip install google-generativeai"
    
    try:
        # Get API key from Streamlit secrets
        api_key = st.secrets.get("GEMINI_API_KEY", None)
        if not api_key:
            return "⚠️ Gemini API key not found. Please add GEMINI_API_KEY to your Streamlit secrets."
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Create the model
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = f"""You are a code analysis expert. Analyze the following {language} code and its Abstract Syntax Tree summary.

Code:
```{language.lower()}
{code}
```

AST Summary:
{ast_summary}

Please provide:
1. A brief overview of what the code does
2. Potential bugs or issues (if any)
3. Code quality observations
4. Suggestions for improvement (if applicable)

Keep your analysis concise and practical."""

        response = model.generate_content(prompt)
        
        return response.text
    
    except Exception as e:
        return f"❌ Error calling Gemini API: {str(e)}"


def main():
    st.set_page_config(
        page_title="Multi-Language Code Analyzer",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Multi-Language Code Analyzer")
    st.markdown("Parse and visualize Abstract Syntax Trees using Tree-sitter")
    
    # Initialize parsers
    with st.spinner("Initializing parsers..."):
        init_status = initialize_parsers()
        if not init_status["success"]:
            st.error(f"❌ Failed to initialize parsers: {init_status['error']}")
            st.info("Please ensure Tree-sitter grammars are properly built. See README for instructions.")
            st.stop()
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Language selection
    language = st.sidebar.selectbox(
        "Select Programming Language",
        options=list(SUPPORTED_LANGUAGES.keys()),
        index=0
    )
    
    # LLM analysis option
    enable_llm = st.sidebar.checkbox(
        "🤖 Enable LLM Analysis",
        value=False,
        help="Use AI to analyze code for bugs and improvements"
    )
    
    if enable_llm and not GEMINI_AVAILABLE:
        st.sidebar.warning("⚠️ Google Generative AI library not installed. LLM features disabled.")
        enable_llm = False
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "💡 **Tip:** Upload a file or paste code below, then click 'Analyze' to see the AST visualization."
    )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Input Code")
        
        # File upload option
        uploaded_file = st.file_uploader(
            "Upload a code file (optional)",
            type=['py', 'js', 'java', 'c', 'cpp', 'h', 'hpp'],
            help="Supported file types: .py, .js, .java, .c, .cpp, .h, .hpp"
        )
        
        # Text area for code input
        if uploaded_file is not None:
            try:
                code_input = uploaded_file.read().decode('utf-8')
                st.success(f"✅ Loaded file: {uploaded_file.name}")
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
                code_input = ""
        else:
            code_input = ""
        
        code = st.text_area(
            "Or paste your code here:",
            value=code_input,
            height=400,
            placeholder=f"Paste your {language} code here...",
            help="Enter or paste the code you want to analyze"
        )
    
    with col2:
        st.subheader("📊 Analysis Options")
        
        show_ast_text = st.checkbox(
            "Show AST as text",
            value=False,
            help="Display the full AST in text format"
        )
        
        max_depth = st.slider(
            "Maximum visualization depth",
            min_value=3,
            max_value=15,
            value=8,
            help="Limit tree depth to avoid overwhelming visualizations"
        )
        
        st.markdown("---")
        analyze_button = st.button("🔍 Analyze Code", type="primary", use_container_width=True)
    
    # Analysis section
    if analyze_button:
        if not code.strip():
            st.warning("⚠️ Please enter some code to analyze.")
            return
        
        try:
            with st.spinner(f"Parsing {language} code..."):
                # Parse the code
                parse_result = parse_code(code, language)
                
                if not parse_result["success"]:
                    st.error(f"❌ Parse Error: {parse_result['error']}")
                    return
                
                tree = parse_result["tree"]
                root_node = tree.root_node
                
                # Success message
                st.success(f"✅ Successfully parsed {language} code!")
                
                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["📊 AST Visualization", "📋 AST Summary", "🤖 LLM Analysis"])
                
                with tab1:
                    st.subheader("Abstract Syntax Tree Visualization")
                    
                    # Generate and display Graphviz chart
                    with st.spinner("Generating AST visualization..."):
                        dot_graph = ast_to_graphviz(root_node, max_depth=max_depth)
                        st.graphviz_chart(dot_graph, use_container_width=True)
                    
                    # Optional text representation
                    if show_ast_text:
                        with st.expander("📄 View AST as Text"):
                            st.text(root_node.sexp())
                
                with tab2:
                    st.subheader("AST Summary")
                    
                    # Get summary information
                    summary = get_ast_summary(root_node)
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Total Nodes", summary["total_nodes"])
                    with col_b:
                        st.metric("Tree Depth", summary["max_depth"])
                    with col_c:
                        st.metric("Top-level Nodes", len(summary["top_level_nodes"]))
                    
                    st.markdown("#### Top-Level AST Nodes")
                    if summary["top_level_nodes"]:
                        st.table({
                            "Node Type": [node["type"] for node in summary["top_level_nodes"]],
                            "Start Position": [f"{node['start'][0]}:{node['start'][1]}" for node in summary["top_level_nodes"]],
                            "End Position": [f"{node['end'][0]}:{node['end'][1]}" for node in summary["top_level_nodes"]]
                        })
                    else:
                        st.info("No top-level nodes found.")
                    
                    # Common node types
                    if summary["node_types"]:
                        with st.expander("📊 Node Type Distribution"):
                            sorted_types = sorted(
                                summary["node_types"].items(),
                                key=lambda x: x[1],
                                reverse=True
                            )[:10]
                            st.bar_chart({node_type: count for node_type, count in sorted_types})
                
                with tab3:
                    st.subheader("AI-Powered Code Analysis")
                    
                    if not enable_llm:
                        st.info("🤖 Enable LLM Analysis in the sidebar to use this feature.")
                    else:
                        with st.spinner("Analyzing code with AI..."):
                            ast_summary_text = f"""
Total Nodes: {summary['total_nodes']}
Tree Depth: {summary['max_depth']}
Top-level Nodes: {', '.join([n['type'] for n in summary['top_level_nodes'][:10]])}
"""
                            llm_response = analyze_with_llm(code, language, ast_summary_text)
                            st.markdown(llm_response)
        
        except Exception as e:
            st.error(f"❌ Unexpected Error: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.code(traceback.format_exc())
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.9em;'>
        Built with Streamlit and Tree-sitter | 
        <a href='https://tree-sitter.github.io/tree-sitter/'>Tree-sitter Documentation</a>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()