#!/bin/bash

# Multi-Language Code Analyzer Setup Script
# This script automates the setup process

set -e

echo "================================================"
echo "  Multi-Language Code Analyzer Setup"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python installation
echo "📋 Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi
echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"

# Check Git installation
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed${NC}"
    echo "Please install Git to continue"
    exit 1
fi
echo -e "${GREEN}✓ Git found: $(git --version)${NC}"

# Check C compiler
if ! command -v gcc &> /dev/null && ! command -v clang &> /dev/null; then
    echo -e "${YELLOW}⚠️  Warning: No C compiler found${NC}"
    echo "You may need to install:"
    echo "  - macOS: xcode-select --install"
    echo "  - Linux: sudo apt-get install build-essential"
    echo "  - Windows: Microsoft Visual C++ Build Tools"
fi

echo ""
echo "📦 Installing Python dependencies..."
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Dependencies installed${NC}"

echo ""
echo "🔨 Building Tree-sitter grammars..."
python3 build_grammars.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to build grammars${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Grammars built successfully${NC}"

echo ""
echo "📁 Creating directories..."
mkdir -p .streamlit
mkdir -p examples

echo ""
echo "📝 Creating example secrets file..."
if [ ! -f .streamlit/secrets.toml ]; then
    cat > .streamlit/secrets.toml.example << 'EOF'
# Copy this file to secrets.toml and add your actual API key
# DO NOT commit secrets.toml to version control!

OPENAI_API_KEY = "sk-your-api-key-here"
EOF
    echo -e "${GREEN}✓ Created .streamlit/secrets.toml.example${NC}"
    echo -e "${YELLOW}  To enable LLM features, copy to secrets.toml and add your OpenAI API key${NC}"
else
    echo -e "${GREEN}✓ Secrets file already exists${NC}"
fi

echo ""
echo "================================================"
echo -e "${GREEN}✅ Setup completed successfully!${NC}"
echo "================================================"
echo ""
echo "🚀 To run the application:"
echo "   streamlit run app.py"
echo ""
echo "📚 For more information, see README.md"
echo ""