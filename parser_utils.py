"""
Tree-sitter parsing utilities for multi-language code analysis
Updated for Tree-sitter v0.22+ (Pip Package Based)
"""

import streamlit as st
from collections import Counter
from typing import Dict, Any, Optional

# Global cache
_parsers: Dict[str, Any] = {}
LANGUAGE_MODULES = {}

try:
    from tree_sitter import Language, Parser, Node
    import tree_sitter_python
    import tree_sitter_javascript
    import tree_sitter_java
    import tree_sitter_c
    import tree_sitter_cpp
    
    TREE_SITTER_AVAILABLE = True
    
    # Define available modules
    LANGUAGE_MODULES = {
        "Python": tree_sitter_python,
        "JavaScript": tree_sitter_javascript,
        "Java": tree_sitter_java,
        "C": tree_sitter_c,
        "C++": tree_sitter_cpp
    }
except ImportError as e:
    TREE_SITTER_AVAILABLE = False
    Language = None
    Parser = None
    Node = None
    IMPORT_ERROR = str(e)

# FIX: Ensure this is a dictionary so app.py can call .keys() on it
SUPPORTED_LANGUAGES = LANGUAGE_MODULES if TREE_SITTER_AVAILABLE else {}

def initialize_parsers() -> Dict[str, Any]:
    """
    Initialize Tree-sitter parsers using installed pip packages.
    """
    if not TREE_SITTER_AVAILABLE:
        return {
            "success": False,
            "error": f"Tree-sitter packages not found. Error: {globals().get('IMPORT_ERROR', 'Unknown error')}. Please install: pip install tree-sitter tree-sitter-python tree-sitter-javascript tree-sitter-java tree-sitter-c tree-sitter-cpp"
        }
    
    try:
        # Pre-load parsers
        for name, module in LANGUAGE_MODULES.items():
            try:
                # Valid for tree-sitter 0.22+
                lang = Language(module.language())
                parser = Parser(lang)
                _parsers[name] = parser
            except Exception as e:
                print(f"Warning: Could not load {name}: {e}")
        
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def parse_code(code: str, language_display_name: str) -> Dict[str, Any]:
    if not TREE_SITTER_AVAILABLE:
        return {"success": False, "error": "Tree-sitter not available."}

    if language_display_name not in _parsers:
        # Try to initialize on demand
        if language_display_name in LANGUAGE_MODULES:
            try:
                module = LANGUAGE_MODULES[language_display_name]
                lang = Language(module.language())
                parser = Parser(lang)
                _parsers[language_display_name] = parser
            except Exception as e:
                return {"success": False, "error": f"Failed to load parser: {str(e)}"}
        else:
            return {"success": False, "error": f"Unsupported language: {language_display_name}"}
    
    parser = _parsers[language_display_name]
    
    try:
        tree = parser.parse(bytes(code, "utf8"))
        return {"success": True, "tree": tree}
    except Exception as e:
        return {"success": False, "error": f"Parse error: {str(e)}"}

def ast_to_graphviz(root_node, max_depth: int = 10) -> str:
    dot_lines = [
        "digraph AST {",
        "  rankdir=TB;",
        "  node [shape=box, style=rounded, fontname=Arial];",
        "  edge [fontname=Arial, fontsize=10];",
        ""
    ]
    
    node_counter = [0]
    
    def add_node(node, parent_id: Optional[int] = None, depth: int = 0) -> int:
        if depth > max_depth:
            return -1
        
        current_id = node_counter[0]
        node_counter[0] += 1
        
        node_type = node.type.replace('"', '\\"')
        
        if node.is_named:
            color = "#E3F2FD"
            border_color = "#1976D2"
        else:
            color = "#F5F5F5"
            border_color = "#757575"
        
        dot_lines.append(
            f'  node{current_id} [label="{node_type}", '
            f'fillcolor="{color}", color="{border_color}", style="rounded,filled"];'
        )
        
        if parent_id is not None:
            dot_lines.append(f'  node{parent_id} -> node{current_id};')
        
        for child in node.children:
            add_node(child, current_id, depth + 1)
        
        return current_id
    
    add_node(root_node)
    dot_lines.append("}")
    return "\n".join(dot_lines)

def get_ast_summary(root_node) -> Dict[str, Any]:
    node_types = Counter()
    total_nodes = [0]
    max_depth = [0]
    top_level_nodes = []
    
    def traverse(node, depth: int = 0):
        total_nodes[0] += 1
        max_depth[0] = max(max_depth[0], depth)
        
        if node.is_named:
            node_types[node.type] += 1
        
        if depth == 1 and node.is_named:
            top_level_nodes.append({
                "type": node.type,
                "start": (node.start_point.row + 1, node.start_point.column),
                "end": (node.end_point.row + 1, node.end_point.column)
            })
        
        for child in node.children:
            traverse(child, depth + 1)
    
    traverse(root_node)
    
    return {
        "total_nodes": total_nodes[0],
        "max_depth": max_depth[0],
        "node_types": dict(node_types),
        "top_level_nodes": top_level_nodes
    }