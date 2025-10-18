# Quick Start Guide

This guide will help you get BionicMemory up and running in minutes.

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

Note: This will install FastAPI, ChromaDB, and other required packages. The full installation may take a few minutes.

2. **Configure your environment:**
```bash
cp .env.example .env
```

Edit `.env` and set your OpenAI API key (required for chat completions):
```bash
OPENAI_API_KEY=sk-your-key-here
```

## Running the Server

Start the BionicMemory server:

```bash
python main.py
```

The server will start on http://localhost:8000

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
Initializing BionicMemory System...
Loading embedding model...
BionicMemory System initialized successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Testing the System

### 1. Health Check

```bash
curl http://localhost:8000/health
```

### 2. Add Memories

```bash
curl -X POST http://localhost:8000/v1/memories \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "content": "Python is a versatile programming language",
    "metadata": {"topic": "programming"}
  }'
```

### 3. Query Memories

```bash
curl -X POST http://localhost:8000/v1/memories/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "query": "programming languages",
    "n_results": 5
  }'
```

### 4. Get Memory Statistics

```bash
curl http://localhost:8000/v1/memories/stats/user123
```

### 5. Chat with Memory (requires OpenAI API key)

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "What do you remember about programming?"}
    ],
    "user": "user123"
  }'
```

## Running Tests

Test core functionality without external dependencies:

```bash
PYTHONPATH=. python tests/test_core.py
```

Test the API (requires server running):

```bash
python examples/test_api.py
```

## Understanding Memory Temperature

When you add or query memories, you'll see a "temperature" value (0.0 to 1.0):

- **🔥 Hot (>0.7)**: Recently created or accessed memories
- **🌡️ Warm (0.3-0.7)**: Memories that are cooling down
- **❄️ Cold (<0.3)**: Old, rarely accessed memories
- **Forgotten (<0.01)**: Memories below threshold are automatically removed

## Memory Lifecycle Example

```python
# Add a new memory (temperature = 1.0) 🔥
POST /v1/memories {"content": "Important fact"}

# Wait some time without accessing it
# Temperature decays: 1.0 → 0.7 → 0.3 → 0.1 (cooling down)

# Access the memory
POST /v1/memories/query {"query": "important"}
# Temperature boosts: 0.1 → 0.4 (warmed up!) 🌡️

# Keep accessing it
# Temperature stays high: 0.4 → 0.7 → 0.9 (use it!) 🔥

# Stop accessing it
# Eventually: 0.9 → 0.5 → 0.1 → 0.005 → forgotten ❄️
```

## Features Demonstration

### User Isolation

Each user has completely separate memories:

```bash
# User1's memories
curl -X POST http://localhost:8000/v1/memories \
  -d '{"user_id": "user1", "content": "User1 private info"}'

# User2's memories
curl -X POST http://localhost:8000/v1/memories \
  -d '{"user_id": "user2", "content": "User2 private info"}'

# Query as user1 - only sees their own memories
curl -X POST http://localhost:8000/v1/memories/query \
  -d '{"user_id": "user1", "query": "info"}'
```

### Clustering Suppression

Add similar memories and see them merge:

```bash
# Add first memory
curl -X POST http://localhost:8000/v1/memories \
  -d '{"user_id": "test", "content": "Python is great"}'
# Response: {"memory_id": "abc123", "status": "added"}

# Add similar memory
curl -X POST http://localhost:8000/v1/memories \
  -d '{"user_id": "test", "content": "Python is awesome"}'
# Response: {"memory_id": "abc123", "status": "merged", "similarity": 0.95}
# Instead of duplicate, it boosts the existing memory!
```

## Troubleshooting

### "Module not found" errors

Make sure you installed dependencies:
```bash
pip install -r requirements.txt
```

### Server won't start

Check if port 8000 is available:
```bash
lsof -i :8000
# If occupied, change PORT in .env
```

### Chat completions fail

Ensure your OpenAI API key is set in `.env`:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [examples/](examples/) for more usage examples
- Explore the [bionicmemory/](bionicmemory/) source code
- Customize settings in `.env` for your use case

## API Documentation

Once the server is running, visit:
- http://localhost:8000/docs - Interactive API documentation (Swagger UI)
- http://localhost:8000/redoc - Alternative API documentation (ReDoc)

Enjoy using BionicMemory! 🧠✨
