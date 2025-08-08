#!/bin/bash

# DataSoph AI - Professional Data Science Platform Setup Script
# Version: 2.0.0

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Emojis
ROCKET="🚀"
CHECK="✅"
CROSS="❌"
WARNING="⚠️"
INFO="ℹ️"
SPARKLE="✨"

echo -e "${BLUE}${ROCKET} DataSoph AI - Professional Data Science Platform${NC}"
echo -e "${BLUE}=================================================${NC}"
echo -e "${CYAN}World's Most Advanced AI Data Scientist${NC}"
echo ""

# Check if script is run from project root
if [ ! -f "package.json" ] && [ ! -f "backend/app/main.py" ]; then
    echo -e "${RED}${CROSS} Error: Please run this script from the DataSoph AI project root directory${NC}"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check version
check_version() {
    local cmd=$1
    local min_version=$2
    local current_version=$($cmd 2>/dev/null)
    echo -e "${INFO} $cmd: $current_version"
}

echo -e "${PURPLE}${SPARKLE} Checking Prerequisites...${NC}"
echo ""

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}${CHECK} Node.js: $NODE_VERSION${NC}"
else
    echo -e "${RED}${CROSS} Node.js not found. Please install Node.js 18+ from https://nodejs.org${NC}"
    exit 1
fi

# Check npm
if command_exists npm; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}${CHECK} npm: $NPM_VERSION${NC}"
else
    echo -e "${RED}${CROSS} npm not found. Please install npm${NC}"
    exit 1
fi

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}${CHECK} Python: $PYTHON_VERSION${NC}"
elif command_exists python; then
    PYTHON_VERSION=$(python --version)
    echo -e "${GREEN}${CHECK} Python: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python"
else
    echo -e "${RED}${CROSS} Python not found. Please install Python 3.8+ from https://python.org${NC}"
    exit 1
fi

# Set Python command
PYTHON_CMD=${PYTHON_CMD:-"python3"}

# Check pip
if command_exists pip3; then
    PIP_VERSION=$(pip3 --version)
    echo -e "${GREEN}${CHECK} pip: $PIP_VERSION${NC}"
    PIP_CMD="pip3"
elif command_exists pip; then
    PIP_VERSION=$(pip --version)
    echo -e "${GREEN}${CHECK} pip: $PIP_VERSION${NC}"
    PIP_CMD="pip"
else
    echo -e "${RED}${CROSS} pip not found. Please install pip${NC}"
    exit 1
fi

# Check Git
if command_exists git; then
    GIT_VERSION=$(git --version)
    echo -e "${GREEN}${CHECK} Git: $GIT_VERSION${NC}"
else
    echo -e "${YELLOW}${WARNING} Git not found. You may need it for version control${NC}"
fi

echo ""
echo -e "${PURPLE}${SPARKLE} Starting Installation...${NC}"
echo ""

# Create virtual environment for backend
echo -e "${BLUE}${INFO} Setting up Python virtual environment...${NC}"
cd backend

if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    echo -e "${GREEN}${CHECK} Virtual environment created${NC}"
else
    echo -e "${YELLOW}${WARNING} Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Upgrade pip in virtual environment
$PIP_CMD install --upgrade pip

# Install backend dependencies
echo -e "${BLUE}${INFO} Installing Python dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    $PIP_CMD install -r requirements.txt
    echo -e "${GREEN}${CHECK} Python dependencies installed${NC}"
else
    echo -e "${YELLOW}${WARNING} requirements.txt not found, installing essential packages...${NC}"
    $PIP_CMD install fastapi uvicorn python-multipart python-dotenv httpx pandas numpy scipy scikit-learn matplotlib seaborn plotly
fi

# Create uploads directory
if [ ! -d "uploads" ]; then
    mkdir uploads
    echo -e "${GREEN}${CHECK} Uploads directory created${NC}"
fi

# Go back to project root
cd ..

# Setup frontend
echo -e "${BLUE}${INFO} Setting up frontend dependencies...${NC}"
if [ -d "frontend" ]; then
    cd frontend
    
    # Install dependencies
    echo -e "${BLUE}${INFO} Installing Node.js dependencies...${NC}"
    npm install
    echo -e "${GREEN}${CHECK} Frontend dependencies installed${NC}"
    
    cd ..
else
    echo -e "${RED}${CROSS} Frontend directory not found${NC}"
    exit 1
fi

# Create environment file if it doesn't exist
echo -e "${BLUE}${INFO} Setting up environment configuration...${NC}"
if [ ! -f "backend/.env" ]; then
    if [ -f "backend/env.example" ]; then
        cp backend/env.example backend/.env
        echo -e "${GREEN}${CHECK} Environment file created from template${NC}"
    else
        # Create basic .env file
        cat > backend/.env << EOL
# DataSoph AI Configuration
APP_NAME="DataSoph AI"
APP_VERSION="2.0.0"
DEBUG=true

# OpenRouter API (for AI capabilities)
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=anthropic/claude-3-sonnet

# File Upload Settings
MAX_FILE_SIZE_MB=100
UPLOAD_DIRECTORY=./uploads

# CORS Settings
CORS_ORIGINS=["http://localhost:3000"]

# Database (Optional - for production)
# DATABASE_URL=postgresql://user:password@localhost/datasoph_ai
EOL
        echo -e "${GREEN}${CHECK} Basic environment file created${NC}"
    fi
    echo -e "${YELLOW}${WARNING} Please edit backend/.env with your API keys${NC}"
else
    echo -e "${YELLOW}${WARNING} Environment file already exists${NC}"
fi

# Create startup scripts
echo -e "${BLUE}${INFO} Creating startup scripts...${NC}"

# Backend startup script
cat > start-backend.sh << 'EOL'
#!/bin/bash
echo "🚀 Starting DataSoph AI Backend..."
cd backend
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
python main.py
EOL

# Frontend startup script
cat > start-frontend.sh << 'EOL'
#!/bin/bash
echo "🚀 Starting DataSoph AI Frontend..."
cd frontend
npm start
EOL

# Make scripts executable
chmod +x start-backend.sh start-frontend.sh

echo -e "${GREEN}${CHECK} Startup scripts created${NC}"

# Create development script
cat > dev.sh << 'EOL'
#!/bin/bash
echo "🚀 Starting DataSoph AI Development Environment..."
echo "Starting backend and frontend concurrently..."

# Function to kill background processes on exit
cleanup() {
    echo "Stopping services..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set trap to cleanup on script exit
trap cleanup EXIT INT TERM

# Start backend in background
echo "Starting backend..."
cd backend
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
python main.py &

# Wait a moment for backend to start
sleep 3

# Start frontend in background
echo "Starting frontend..."
cd ../frontend
npm start &

# Wait for processes
wait
EOL

chmod +x dev.sh

echo -e "${GREEN}${CHECK} Development script created${NC}"

# Installation complete
echo ""
echo -e "${GREEN}${SPARKLE}========================================${NC}"
echo -e "${GREEN}${CHECK} DataSoph AI Installation Complete!${NC}"
echo -e "${GREEN}${SPARKLE}========================================${NC}"
echo ""

echo -e "${CYAN}Next Steps:${NC}"
echo ""
echo -e "${BLUE}1.${NC} Configure your API keys:"
echo -e "   ${YELLOW}nano backend/.env${NC}"
echo ""
echo -e "${BLUE}2.${NC} Start the development environment:"
echo -e "   ${YELLOW}./dev.sh${NC}"
echo ""
echo -e "${BLUE}3.${NC} Or start services individually:"
echo -e "   ${YELLOW}./start-backend.sh${NC}   # Backend: http://localhost:8000"
echo -e "   ${YELLOW}./start-frontend.sh${NC}  # Frontend: http://localhost:3000"
echo ""

echo -e "${CYAN}Useful URLs:${NC}"
echo -e "${BLUE}• Frontend:${NC} http://localhost:3000"
echo -e "${BLUE}• Backend API:${NC} http://localhost:8000"
echo -e "${BLUE}• API Documentation:${NC} http://localhost:8000/docs"
echo -e "${BLUE}• Health Check:${NC} http://localhost:8000/health"
echo ""

echo -e "${CYAN}Required API Keys:${NC}"
echo -e "${BLUE}• OpenRouter:${NC} Get your API key at https://openrouter.ai/"
echo -e "${BLUE}• Configuration:${NC} Edit backend/.env file"
echo ""

echo -e "${CYAN}Features Available:${NC}"
echo -e "${GREEN}${CHECK}${NC} Professional Dashboard"
echo -e "${GREEN}${CHECK}${NC} AI Assistant Chat"
echo -e "${GREEN}${CHECK}${NC} Data Workspace"
echo -e "${GREEN}${CHECK}${NC} Analysis Studio"
echo -e "${GREEN}${CHECK}${NC} Code Environment"
echo -e "${GREEN}${CHECK}${NC} Export Center"
echo ""

echo -e "${PURPLE}${SPARKLE} Welcome to DataSoph AI - The Future of Data Science! ${SPARKLE}${NC}"
echo -e "${CYAN}Documentation: https://docs.datasoph.ai${NC}"
echo -e "${CYAN}Support: support@datasoph.ai${NC}"
echo "" 