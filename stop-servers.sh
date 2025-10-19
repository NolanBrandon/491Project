#!/bin/bash

# Colors for output
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Stopping EasyFitness servers...${NC}"

# Stop backend
if [ -f /tmp/easyfitness_backend.pid ]; then
    BACKEND_PID=$(cat /tmp/easyfitness_backend.pid)
    if ps -p $BACKEND_PID > /dev/null; then
        echo -e "${RED}Stopping Django backend (PID: $BACKEND_PID)...${NC}"
        kill $BACKEND_PID
        rm /tmp/easyfitness_backend.pid
    else
        echo "Backend process not running"
        rm /tmp/easyfitness_backend.pid
    fi
else
    echo "No backend PID file found"
fi

# Stop frontend
if [ -f /tmp/easyfitness_frontend.pid ]; then
    FRONTEND_PID=$(cat /tmp/easyfitness_frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null; then
        echo -e "${RED}Stopping Next.js frontend (PID: $FRONTEND_PID)...${NC}"
        kill $FRONTEND_PID
        rm /tmp/easyfitness_frontend.pid
    else
        echo "Frontend process not running"
        rm /tmp/easyfitness_frontend.pid
    fi
else
    echo "No frontend PID file found"
fi

echo -e "${BLUE}Servers stopped!${NC}"
