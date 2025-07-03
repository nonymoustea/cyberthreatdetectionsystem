#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}   🛡️  AI Email Threat Detector${NC}"
echo -e "${BLUE}============================================${NC}"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}❌ Python is not installed or not in PATH${NC}"
        echo "Please install Python from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check if required files exist
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ app.py not found in current directory${NC}"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ requirements.txt not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python found: $($PYTHON_CMD --version)${NC}"
echo -e "${YELLOW}📦 Installing/updating dependencies...${NC}"
echo

# Install dependencies
if ! $PYTHON_CMD -m pip install -r requirements.txt; then
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

echo
echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
echo -e "${BLUE}🚀 Starting AI Email Threat Detector...${NC}"
echo
echo -e "${YELLOW}Navigate to: http://localhost:5050${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo

# Start the Flask application
$PYTHON_CMD app.py

echo
echo -e "${RED}🛑 Server stopped${NC}" 