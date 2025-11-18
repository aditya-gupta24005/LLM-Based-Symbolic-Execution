"""
Script to build Tree-sitter grammar libraries for tree-sitter v0.21+
This version uses the new tree-sitter API
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil


GRAMMARS = {
    "python": "https://github.com/tree-sitter/tree-sitter-python",
    "javascript": "https://github.com/tree-sitter/tree-sitter-javascript",
    "java": "https://github.com/tree-sitter/tree-sitter-java",
    "c": "https://github.com/tree-sitter/tree-sitter-c",
    "cpp": "https://github.com/tree-sitter/tree-sitter-cpp"
}


def run_command(cmd, cwd=None):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
            shell=isinstance(cmd, str)
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def build_language_library(lang_name, repo_path, output_dir):
    """Build a single language library using tree-sitter CLI"""
    try:
        # Find the grammar directory (usually 'src' or root)
        grammar_path = repo_path / "src"
        if not grammar_path.exists():
            grammar_path = repo_path
        
        # Look for parser.c or grammar.js
        parser_c = grammar_path / "parser.c"
        grammar_js = grammar_path / "grammar.js"
        
        if not parser_c.exists() and not grammar_js.exists():
            return False, f"No parser.c or grammar.js found in {grammar_path}"
        
        # Create Python bindings using ctypes
        print(f"    Building {lang_name} library...")
        
        # Use tree-sitter's Language class directly with the new API
        from tree_sitter import Language
        
        # The new API expects just the path to the grammar directory
        try:
            # For tree-sitter >= 0.21, we use Language() constructor directly
            language = Language(str(grammar_path))
            
            # Save the language object
            output_file = output_dir / f"{lang_name}.so"
            
            # We can't directly save Language objects, so we'll use a different approach
            # Store the path instead
            path_file = output_dir / f"{lang_name}.path"
            path_file.write_text(str(grammar_path))
            
            return True, f"Language path saved to {path_file}"
            
        except Exception as e:
            return False, f"Failed to create Language: {e}"
            
    except Exception as e:
        return False, f"Build error: {e}"


def main():
    print("🔨 Building Tree-sitter Grammars (New API)")
    print("=" * 50)
    
    # Check tree-sitter version
    try:
        import tree_sitter
        version = getattr(tree_sitter, '__version__', 'unknown')
        print(f"📌 Tree-sitter version: {version}")
        
        # Check if we have Language class
        from tree_sitter import Language
        print(f"✓ Language class available")
        
    except ImportError:
        print("❌ tree-sitter not installed")
        print("Run: pip install tree-sitter")
        return False
    
    # Create grammars directory
    grammars_dir = Path("grammars")
    grammars_dir.mkdir(exist_ok=True)
    
    # Clone or update grammar repositories
    print("\n📦 Downloading grammar repositories...")
    for lang_name, repo_url in GRAMMARS.items():
        repo_dir = grammars_dir / f"tree-sitter-{lang_name}"
        
        if repo_dir.exists():
            print(f"  ✓ {lang_name}: Repository already exists")
        else:
            print(f"  ⬇️  {lang_name}: Cloning from {repo_url}")
            success, output = run_command(
                ["git", "clone", "--depth", "1", repo_url, str(repo_dir)]
            )
            if success:
                print(f"  ✓ {lang_name}: Clone successful")
            else:
                print(f"  ✗ {lang_name}: Clone failed - {output}")
                return False
    
    # With tree-sitter 0.25+, we use a different approach
    print("\n🔧 Setting up language parsers...")
    print("ℹ️  For tree-sitter 0.25+, we'll use dynamic loading")
    
    # Create a manifest file that tells parser_utils where to find grammars
    manifest = {}
    for lang_name in GRAMMARS.keys():
        repo_dir = grammars_dir / f"tree-sitter-{lang_name}"
        src_dir = repo_dir / "src"
        if not src_dir.exists():
            src_dir = repo_dir
        manifest[lang_name] = str(src_dir.absolute())
    
    # Save manifest
    import json
    manifest_path = grammars_dir / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✓ Created grammar manifest: {manifest_path}")
    print(f"  Contains paths to {len(manifest)} language grammars")
    
    return True


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Tree-sitter Grammar Setup (v0.25+ Compatible)")
    print("=" * 50)
    
    # Check if git is available
    success, _ = run_command(["git", "--version"])
    if not success:
        print("❌ Error: git is not installed or not in PATH")
        print("Please install git to continue.")
        sys.exit(1)
    
    # Run the build process
    if main():
        print("\n✅ Setup completed successfully!")
        print("\n🚀 You can now run the app with:")
        print("   streamlit run app.py")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)