# 🔍 Multi-Language Code Analyzer

A production-ready Streamlit web application for parsing and visualizing Abstract Syntax Trees (AST) using Tree-sitter, with optional AI-powered code analysis.

## Features

- ✅ **Multi-Language Support**: Python, JavaScript, Java, C, C++
- 📊 **AST Visualization**: Interactive Graphviz charts
- 📋 **AST Analysis**: Detailed statistics and node summaries
- 🤖 **AI Code Review**: Optional LLM-powered analysis (requires Gemini API key)
- 📁 **File Upload**: Support for various file types
- 🎨 **Clean UI**: Intuitive Streamlit interface
- ☁️ **Cloud Ready**: Deployable on Streamlit Cloud

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Git (for grammar building)
- C compiler (gcc/clang) - required for building Tree-sitter grammars

### Installation

1. **Clone or download this repository**

```bash
git clone <your-repo-url>
cd code-analyzer
```

2. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

3. **Build Tree-sitter grammars**

```bash
python build_grammars.py
```

This script will:
- Clone Tree-sitter grammar repositories for all supported languages
- Compile them into a single shared library (`grammars/my-languages.so`)
- Take 2-5 minutes to complete

4. **Run the application**

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
code-analyzer/
├── app.py                  # Main Streamlit application
├── parser_utils.py         # Tree-sitter parsing utilities
├── build_grammars.py       # Grammar build script
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── grammars/              # Grammar files (created by build script)
    ├── tree-sitter-python/
    ├── tree-sitter-javascript/
    ├── tree-sitter-java/
    ├── tree-sitter-c/
    ├── tree-sitter-cpp/
    └── my-languages.so    # Compiled grammar library
```

## Usage

### Basic Analysis

1. Select your programming language from the dropdown
2. Either:
   - Upload a code file, or
   - Paste code into the text area
3. Click "Analyze Code"
4. View the AST visualization and summary

### Advanced Features

- **Adjust Visualization Depth**: Use the slider to control tree depth (prevents overwhelming visuals)
- **View Text AST**: Enable "Show AST as text" for the raw S-expression format
- **AI Analysis**: Enable "LLM Analysis" in the sidebar for AI-powered code review

### LLM Analysis Setup (Optional)

To enable AI-powered code analysis:

1. Get a Gemini API key from https://aistudio.google.com/app/apikey
2. Create a `.streamlit/secrets.toml` file:

```toml
GEMINI_API_KEY = "your-api-key-here"
```

3. Enable "LLM Analysis" in the sidebar

## Deployment to Streamlit Cloud

### Option 1: With Pre-built Grammars

1. Build grammars locally using `python build_grammars.py`
2. Commit the `grammars/` directory (including `my-languages.so`) to your repository
3. Push to GitHub
4. Deploy on Streamlit Cloud pointing to your repository

### Option 2: Build on Streamlit Cloud

Add a `packages.txt` file to install system dependencies:

```txt
build-essential
git
```

Streamlit Cloud will automatically run `build_grammars.py` if configured properly.

**Note**: Building grammars on Streamlit Cloud can be slow. Pre-building and committing the `.so` file is recommended.

### Setting Secrets on Streamlit Cloud

1. Go to your app settings on Streamlit Cloud
2. Navigate to "Secrets"
3. Add your Gemini API key:

```toml
GEMINI_API_KEY = "your-api-key-here"
```

## Troubleshooting

### Grammar Build Fails

**Problem**: `build_grammars.py` fails with compiler errors

**Solutions**:
- Ensure you have a C compiler installed:
  - **macOS**: Install Xcode Command Line Tools: `xcode-select --install`
  - **Linux**: Install build essentials: `sudo apt-get install build-essential`
  - **Windows**: Install Microsoft Visual C++ Build Tools

### Import Error: tree_sitter

**Problem**: `ModuleNotFoundError: No module named 'tree_sitter'`

**Solution**:
```bash
pip install tree-sitter
```

### Grammar Library Not Found

**Problem**: App shows "Grammar library not found"

**Solution**:
- Run `python build_grammars.py` to build the grammars
- Verify `grammars/my-languages.so` (or `.dylib`/`.dll`) exists

### Parse Errors

**Problem**: Code shows parse errors even when valid

**Solution**:
- Verify you selected the correct language
- Check for syntax errors in your code
- Some edge cases may not be supported by Tree-sitter grammars

## Supported Languages & File Types

| Language   | File Extensions          | Grammar Source                                      |
|------------|-------------------------|-----------------------------------------------------|
| Python     | `.py`                   | tree-sitter/tree-sitter-python                      |
| JavaScript | `.js`                   | tree-sitter/tree-sitter-javascript                  |
| Java       | `.java`                 | tree-sitter/tree-sitter-java                        |
| C          | `.c`, `.h`              | tree-sitter/tree-sitter-c                           |
| C++        | `.cpp`, `.hpp`, `.h`    | tree-sitter/tree-sitter-cpp                         |

## Development

### Adding New Languages

To add support for a new language:

1. Add the grammar URL to `GRAMMARS` in `build_grammars.py`:
```python
GRAMMARS = {
    # ...existing languages...
    "rust": "https://github.com/tree-sitter/tree-sitter-rust"
}
```

2. Add to `SUPPORTED_LANGUAGES` in `parser_utils.py`:
```python
SUPPORTED_LANGUAGES = {
    # ...existing languages...
    "Rust": "rust"
}
```

3. Rebuild grammars: `python build_grammars.py`

### Customizing Visualization

Edit the `ast_to_graphviz()` function in `parser_utils.py` to customize:
- Node colors and styles
- Edge formatting
- Label content
- Graph layout

## Performance Considerations

- **Large Files**: Files over 10,000 lines may take time to parse and visualize
- **Depth Limit**: Default max depth is 8 levels; increase cautiously
- **LLM Calls**: Each analysis consumes API credits; use judiciously

## Dependencies

- **streamlit**: Web application framework
- **tree-sitter**: Parser generator and parsing library
- **graphviz**: Graph visualization
- **pygments**: Syntax highlighting (future use)
- **google-generativeai**: Gemini API client (optional)

## License

This project is provided as-is for educational and commercial use.

## Contributing

Contributions are welcome! Areas for improvement:
- Additional language support
- Enhanced visualization options
- More detailed AST analysis
- Export functionality (PDF, PNG)
- Syntax highlighting in code view

## Credits

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Tree-sitter](https://tree-sitter.github.io/)
- Visualization with [Graphviz](https://graphviz.org/)
- AI analysis via [Google Gemini](https://ai.google.dev/)

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

---

Made with ❤️ using Streamlit and Tree-sitter