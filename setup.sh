#!/bin/bash

# DataSoph AI - Complete Setup Script
# This script sets up the entire DataSoph AI system from scratch

set -e  # Exit on any error

echo "🚀 DataSoph AI - Automated Setup Starting..."
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux"* ]]; then
    OS="Linux"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

print_info "Detected OS: $OS"

# 1. Create necessary directories
print_info "Creating project directories..."
mkdir -p uploads figures reports logs exports temp
print_status "Directories created"

# 2. Check Python installation
print_info "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
    print_status "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 is required but not installed"
    print_info "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# 3. Check Node.js installation
print_info "Checking Node.js installation..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_status "Node.js found: $NODE_VERSION"
else
    print_error "Node.js is required but not installed"
    print_info "Please install Node.js from https://nodejs.org"
    exit 1
fi

# 4. Create Python virtual environment
print_info "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# 5. Activate virtual environment and install Python dependencies
print_info "Installing Python dependencies..."
source venv/bin/activate

# Check if requirements.txt exists, if not create it
if [ ! -f "requirements.txt" ]; then
    print_info "Creating requirements.txt..."
    cat > requirements.txt << 'EOL'
# Core FastAPI and server dependencies
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
python-dotenv==1.0.0

# HTTP and async support
httpx==0.25.2
aiofiles==23.2.1

# Data science and analysis
pandas==2.1.4
numpy==1.24.4
matplotlib==3.7.4
seaborn==0.13.0
scipy==1.11.4
scikit-learn==1.3.2

# Additional data processing
openpyxl==3.1.2
xlrd==2.0.1

# Logging and utilities
pydantic==2.5.2
typing-extensions==4.8.0

# Development dependencies (optional)
pytest==7.4.3
pytest-asyncio==0.21.1
EOL
    print_status "requirements.txt created"
fi

pip install --upgrade pip
pip install -r requirements.txt
print_status "Python dependencies installed"

# 6. Install Node.js dependencies for frontend
print_info "Installing frontend dependencies..."
cd frontend

# Check if package.json exists
if [ ! -f "package.json" ]; then
    print_error "package.json not found in frontend directory"
    exit 1
fi

npm install
print_status "Frontend dependencies installed"

cd ..

# 7. Setup environment file
print_info "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        cp env.example .env
        print_warning "Created .env from env.example - PLEASE UPDATE WITH YOUR API KEYS!"
    else
        print_error "env.example not found - creating basic .env"
        cat > .env << 'EOL'
# DataSoph AI Environment Configuration
OPENROUTER_API_KEY=your-openrouter-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=True
EOL
    fi
else
    print_warning ".env already exists - skipping"
fi

# 8. Test Python imports
print_info "Testing Python imports..."
source venv/bin/activate
python3 -c "
import fastapi
import pandas
import matplotlib
import numpy
import httpx
print('✅ All Python imports successful')
" && print_status "Python environment verified"

# 9. Build frontend (development mode)
print_info "Preparing frontend..."
cd frontend
if command -v npm &> /dev/null; then
    # Don't build in development, just verify dependencies
    npm list --depth=0 > /dev/null 2>&1 && print_status "Frontend dependencies verified"
else
    print_error "npm not found"
    exit 1
fi
cd ..

# 10. Create startup scripts
print_info "Creating startup scripts..."

# Backend startup script
cat > start_backend.sh << 'EOL'
#!/bin/bash
echo "🚀 Starting DataSoph AI Backend..."
cd backend
source ../venv/bin/activate
export OPENROUTER_API_KEY=$(grep OPENROUTER_API_KEY ../.env | cut -d '=' -f2)
python simple_ai_server.py
EOL

# Frontend startup script  
cat > start_frontend.sh << 'EOL'
#!/bin/bash
echo "🚀 Starting DataSoph AI Frontend..."
cd frontend
npm start
EOL

# Combined startup script
cat > start_all.sh << 'EOL'
#!/bin/bash
echo "🚀 Starting DataSoph AI - Full System..."
echo "Starting backend in background..."
./start_backend.sh &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

echo "Waiting 5 seconds for backend to start..."
sleep 5

echo "Starting frontend..."
./start_frontend.sh &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo "🎉 DataSoph AI is starting up!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
EOL

# Make scripts executable
chmod +x start_backend.sh start_frontend.sh start_all.sh
print_status "Startup scripts created"

# 11. Create README for deployment
print_info "Creating deployment README..."
cat > DEPLOYMENT.md << 'EOL'
# DataSoph AI - Deployment Guide

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd DATASOPH_AI
chmod +x setup.sh
./setup.sh
```

### 2. Configure API Keys
Edit `.env` file and add your API keys:
```bash
OPENROUTER_API_KEY=your-openrouter-api-key-here
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### 3. Start the System
```bash
# Start everything
./start_all.sh

# Or start individually
./start_backend.sh    # Backend only
./start_frontend.sh   # Frontend only
```

### 4. Access the Application
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Health**: http://localhost:8000/api/v1/health

## 🔧 Manual Setup

### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENROUTER_API_KEY=your-key-here
python simple_ai_server.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🔑 Required API Keys

### OpenRouter (Primary)
1. Go to https://openrouter.ai/keys
2. Create account and generate API key
3. Add to `.env` as `OPENROUTER_API_KEY`

### OpenAI (Optional)
1. Go to https://platform.openai.com/api-keys
2. Generate API key
3. Add to `.env` as `OPENAI_API_KEY`

## 📁 Project Structure
```
DATASOPH_AI/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── uploads/           # File uploads (auto-created)
├── figures/           # Generated charts (auto-created)
├── reports/           # Analysis reports (auto-created)
├── .env              # Environment variables (YOU CREATE)
├── env.example       # Environment template
└── setup.sh          # Automated setup script
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill processes on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill processes on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### Python Dependencies Issues
```bash
cd DATASOPH_AI
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend Build Issues
```bash
cd frontend
rm -rf node_modules
npm install
```

## 🔐 Security Notes

- Never commit `.env` file to Git
- Keep API keys secure
- Use environment variables in production
- Update dependencies regularly

## 🎯 Features

✅ Intelligent AI chat with OpenRouter/OpenAI
✅ Comprehensive EDA (9-section analysis)
✅ File upload and analysis (CSV, Excel)
✅ Automatic chart generation
✅ HTML table formatting
✅ Downloadable reports
✅ Real-time conversation memory
✅ Multilingual support (Turkish/English)
EOL

print_status "Deployment documentation created"

# 12. Final verification
print_info "Running final verification..."

# Check if all critical files exist
CRITICAL_FILES=(
    "backend/simple_ai_server.py"
    "backend/file_memory.py"
    "backend/comprehensive_eda.py"
    "backend/response_enhancer.py"
    "backend/visualization_generator.py"
    "frontend/src/App.js"
    "frontend/package.json"
    "requirements.txt"
    ".gitignore"
    "env.example"
)

ALL_GOOD=true
for file in "${CRITICAL_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Missing critical file: $file"
        ALL_GOOD=false
    fi
done

if [ "$ALL_GOOD" = true ]; then
    print_status "All critical files present"
else
    print_error "Some critical files are missing"
    exit 1
fi

# 13. Final instructions
echo ""
echo "🎉 DataSoph AI Setup Complete!"
echo "=============================================="
print_status "Setup completed successfully!"
echo ""
print_warning "IMPORTANT NEXT STEPS:"
echo "1. Edit .env file with your actual API keys"
echo "2. Run: ./start_all.sh"
echo "3. Open http://localhost:3000 in browser"
echo ""
print_info "Documentation: See DEPLOYMENT.md for detailed instructions"
print_info "Troubleshooting: Check logs in the console output"
echo ""
echo "Happy coding! 🚀" 