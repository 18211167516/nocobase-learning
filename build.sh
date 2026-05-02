#!/bin/bash

echo "Building NocoBase Learning Platform..."

# Build backend
echo "Building backend..."
cd backend
pip install -r requirements.txt
cd ..

# Build frontend
echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Build complete!"
echo ""
echo "To run the application:"
echo "  Backend: cd backend && uvicorn main:app --reload"
echo "  Frontend: cd frontend && npm run dev"
