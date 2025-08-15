#!/bin/bash

echo "🚀 DATASOPH AI - ULTIMATE STARTUP SCRIPT"
echo "=========================================="

# Kill any existing processes
echo "🔧 Clearing ports..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

# Start backend
echo "📡 Starting backend server..."
cd backend
python final_server.py &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "⏳ Waiting for backend..."
sleep 5

# Test backend
echo "🔍 Testing backend..."
curl -X GET http://localhost:8000/api/v1/health

# Start frontend
echo "🎨 Starting frontend..."
cd ../frontend
npm start &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo "✅ DATASOPH AI STARTED!"
echo "📍 Backend:  http://localhost:8000"
echo "📍 Frontend: http://localhost:3000"
echo ""
echo "🎯 TEST COMMANDS:"
echo "curl -X POST http://localhost:8000/api/v1/ai/chat -H 'Content-Type: application/json' -d '{\"message\":\"merhaba\",\"user_id\":\"test\"}'"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap "echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
