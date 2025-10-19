#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting EasyFitness servers...${NC}"

# Navigate to backend directory
cd /Users/ivanflores/capstone/backend

# Start Django backend
echo -e "${GREEN}Starting Django backend...${NC}"
source easyfitness_env/bin/activate
python manage.py runserver > /tmp/django.log 2>&1 &
BACKEND_PID=$!
echo "Backend running on http://localhost:8000 (PID: $BACKEND_PID)"

# Navigate to frontend directory
cd /Users/ivanflores/capstone/easyfitness

# Start Next.js frontend
echo -e "${GREEN}Starting Next.js frontend...${NC}"
npm run dev > /tmp/nextjs.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend running on http://localhost:3000 (PID: $FRONTEND_PID)"

# Save PIDs to file for easy stopping later
echo $BACKEND_PID > /tmp/easyfitness_backend.pid
echo $FRONTEND_PID > /tmp/easyfitness_frontend.pid

echo -e "${BLUE}Servers started!${NC}"
echo "Backend: http://localhost:8000 (PID: $BACKEND_PID)"
echo "Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
echo ""
echo "To view logs:"
echo "  Backend:  tail -f /tmp/django.log"
echo "  Frontend: tail -f /tmp/nextjs.log"
echo ""
echo "To stop servers, run: ./stop-servers.sh"
