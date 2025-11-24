# Docker Deployment Troubleshooting Guide

This guide helps you troubleshoot common issues when running the RAG system with Docker.

## Common Issues and Solutions

### 1. Network Error / Could Not Connect to API

**Symptoms:**
- "Network Error: Could not connect to the server"
- "Domain Expert Sorry, I encountered an error: Network Error. Please make sure the RAG API is running."

**Solutions:**
1. Check if the Docker container is running:
   ```bash
   docker-compose ps
   ```

2. View container logs:
   ```bash
   docker-compose logs rag-system
   ```

3. Check if port 8000 is available:
   ```bash
   netstat -an | grep 8000
   ```

4. Rebuild and restart the containers:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

### 2. Container Fails to Start

**Symptoms:**
- Container exits immediately after starting
- Error messages in logs about missing files or dependencies

**Solutions:**
1. Check Docker logs for detailed error messages:
   ```bash
   docker-compose logs --tail=50
   ```

2. Ensure all required files are present:
   - `requirements.txt`
   - `src/rag_system/` directory
   - `Dockerfile.full`

3. Rebuild with no cache:
   ```bash
   docker-compose build --no-cache
   docker-compose up
   ```

### 3. Frontend Not Loading

**Symptoms:**
- Blank page when accessing http://localhost:8000
- Console errors about missing files

**Solutions:**
1. Check if the frontend files were built correctly:
   ```bash
   # In the container, check if frontend files exist
   docker-compose exec rag-system ls -la /app/frontend
   ```

2. Rebuild the frontend:
   ```bash
   # Go to the frontend directory
   cd src/rag_system/frontend
   npm install
   npm run build
   ```

### 4. API Returns 404 Errors

**Symptoms:**
- API endpoints return 404 Not Found
- Query functionality not working

**Solutions:**
1. Check if the API server is running:
   ```bash
   docker-compose exec rag-system ps aux | grep python
   ```

2. Verify API endpoints:
   ```bash
   curl http://localhost:8000/api
   curl http://localhost:8000/health
   ```

### 5. Initialization Issues

**Symptoms:**
- No documents available for querying
- "No existing index found" messages

**Solutions:**
1. Check if initialization completed:
   ```bash
   docker-compose logs rag-system | grep "initializing"
   ```

2. Manually initialize the system:
   ```bash
   docker-compose exec rag-system python docker_init.py
   ```

## Debugging Commands

### View Running Containers
```bash
docker-compose ps
```

### View Container Logs
```bash
# View all logs
docker-compose logs

# View recent logs
docker-compose logs --tail=50

# Follow logs in real-time
docker-compose logs -f
```

### Execute Commands in Container
```bash
# Access container shell
docker-compose exec rag-system /bin/bash

# Check Python processes
docker-compose exec rag-system ps aux | grep python

# List files in frontend directory
docker-compose exec rag-system ls -la /app/frontend
```

### Restart Services
```bash
# Restart specific service
docker-compose restart rag-system

# Restart all services
docker-compose restart

# Stop and start
docker-compose down
docker-compose up
```

## Port Conflicts

If you get an error about port 8000 being in use:

1. Find the process using port 8000:
   ```bash
   netstat -ano | findstr :8000
   ```

2. Kill the process (Windows):
   ```bash
   taskkill /PID <process_id> /F
   ```

3. Or change the port in docker-compose.yml:
   ```yaml
   ports:
     - "8001:8000"  # Map host port 8001 to container port 8000
   ```

## Volume Issues

If data is not persisting or volumes are not mounting correctly:

1. Check volume mounts:
   ```bash
   docker-compose exec rag-system ls -la /app/data
   docker-compose exec rag-system ls -la /app/indexes
   ```

2. Verify local directories exist:
   ```bash
   ls -la data/
   ls -la indexes/
   ```

3. Create directories if missing:
   ```bash
   mkdir -p data indexes
   ```

## Environment Variables

Ensure environment variables are set correctly:

```bash
# Check environment in container
docker-compose exec rag-system env
```

The Docker setup should have:
- `PYTHONPATH=/app`
- `NODE_ENV=production`

## Testing the Setup

After fixing issues, test the complete setup:

1. Run the test script:
   ```bash
   python test_docker_setup.py
   ```

2. Access the web interface:
   - Open browser to http://localhost:8000
   - Try asking a question like "Who led the Salt Satyagraha?"

3. Test API endpoints:
   ```bash
   curl http://localhost:8000/api
   curl http://localhost:8000/health
   ```

## Need More Help?

If you're still experiencing issues:

1. Share the output of:
   ```bash
   docker-compose logs --tail=100
   docker-compose ps
   ```

2. Check the troubleshooting guide for your specific error message

3. Ensure all prerequisites are installed:
   - Docker Desktop (Windows/Mac)
   - Docker Engine (Linux)
   - Docker Compose