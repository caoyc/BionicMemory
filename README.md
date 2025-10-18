# BionicMemory

基于生物脑仿生、通过牛顿冷却公式模拟艾宾浩斯遗忘规律、仿生实现"用进废退"策略的永久记忆管理系统 - 让每个AI都有记忆，让每个记忆都有温度

A bionic brain-inspired AI memory management system that simulates the Ebbinghaus forgetting curve through Newton's cooling formula and implements a "use it or lose it" strategy.

## 🌟 Features

- **OpenAI-Compatible API Proxy** - FastAPI-based proxy that seamlessly integrates with OpenAI's chat completion API
- **Local Embedding Service** - Uses lightweight transformer models (Qwen2-0.5B or sentence-transformers) for local embedding generation
- **ChromaDB Vector Storage** - Efficient vector database for similarity search and memory retrieval
- **Newton Cooling Memory Decay** - Simulates biological memory decay using Newton's Law of Cooling to model the Ebbinghaus forgetting curve
- **Clustering Suppression** - Intelligent deduplication that merges similar memories and reinforces existing ones
- **Long/Short-Term Memory** - Automatic management of memory lifecycle based on temperature and access patterns
- **User Isolation** - Complete separation of memories between different users
- **Temperature-Based Memory** - Each memory has a "temperature" that indicates its strength and recency

## 🧠 How It Works

### Newton Cooling Formula for Memory Decay

BionicMemory uses Newton's Law of Cooling to simulate how memories naturally fade over time:

```
T(t) = T_ambient + (T_initial - T_ambient) × e^(-k×t)
```

Where:
- `T(t)` is the memory temperature at time t
- `T_ambient` is the ambient temperature (0, representing complete forgetting)
- `T_initial` is the initial temperature (1.0, representing a fresh memory)
- `k` is the decay rate (configurable)
- `t` is the time elapsed since last access

This formula naturally models the Ebbinghaus forgetting curve, where memories decay exponentially over time.

### "Use It or Lose It" Strategy

- **Access Boost**: When a memory is accessed or reinforced, its temperature increases
- **Natural Decay**: Unused memories gradually cool down over time
- **Forgetting Threshold**: Memories below a certain temperature (default 0.01) are forgotten
- **Clustering Suppression**: Similar new memories boost existing ones instead of creating duplicates

### Memory Lifecycle

1. **Creation** (Temperature = 1.0) 🔥
2. **Active Use** (Temperature > 0.7) 🔥
3. **Warm Memory** (Temperature 0.3-0.7) 🌡️
4. **Cooling** (Temperature 0.01-0.3) ❄️
5. **Forgotten** (Temperature < 0.01) ❌

## 🚀 Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/caoyc/BionicMemory.git
cd BionicMemory
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings (especially OPENAI_API_KEY if using chat completions)
```

### Configuration

Edit `.env` to customize:

```bash
# OpenAI API (required for chat completions)
OPENAI_API_KEY=your_key_here
OPENAI_API_BASE=https://api.openai.com/v1

# Server
HOST=0.0.0.0
PORT=8000

# Memory Settings
MEMORY_DECAY_RATE=0.1        # How fast memories cool (0.0-1.0)
MEMORY_THRESHOLD=0.01        # Temperature threshold for forgetting
SHORT_TERM_MEMORY_SIZE=100   # Max short-term memories
LONG_TERM_MEMORY_SIZE=1000   # Max long-term memories

# Embedding Model
EMBEDDING_MODEL=Qwen/Qwen2-0.5B-Instruct  # or sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DEVICE=cpu         # or cuda for GPU

# Storage
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

## 📖 Usage

### Starting the Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### API Endpoints

#### 1. OpenAI-Compatible Chat Completion

```bash
POST /v1/chat/completions
```

Automatically retrieves and injects relevant memories into the conversation context.

Example:
```python
import httpx

response = httpx.post("http://localhost:8000/v1/chat/completions", json={
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "What did we discuss about Python?"}
    ],
    "user": "user123"  # User ID for memory isolation
})
```

#### 2. Add Memory

```bash
POST /v1/memories
```

Example:
```python
response = httpx.post("http://localhost:8000/v1/memories", json={
    "user_id": "user123",
    "content": "Python is great for data science",
    "metadata": {"topic": "programming", "language": "python"}
})
```

Response:
```json
{
    "memory_id": "uuid-here",
    "status": "added"  // or "merged" if similar memory exists
}
```

#### 3. Query Memories

```bash
POST /v1/memories/query
```

Example:
```python
response = httpx.post("http://localhost:8000/v1/memories/query", json={
    "user_id": "user123",
    "query": "programming languages",
    "n_results": 10
})
```

#### 4. Get Memory Statistics

```bash
GET /v1/memories/stats/{user_id}
```

Returns statistics about a user's memories including total count, hot/cold memories, and average temperature.

#### 5. Cleanup Cold Memories

```bash
POST /v1/memories/cleanup
```

Removes memories that have cooled below the threshold.

### Running Examples

1. **API Test**:
```bash
# Start the server first
python main.py

# In another terminal
python examples/test_api.py
```

2. **Memory Decay Visualization**:
```bash
pip install matplotlib
python examples/memory_decay_demo.py
```

This generates a visualization showing how memories decay over time with and without reinforcement.

## 🏗️ Architecture

```
BionicMemory/
├── bionicmemory/
│   ├── api/              # FastAPI application
│   │   └── app.py        # Main API endpoints
│   ├── core/             # Core functionality
│   │   ├── memory.py     # Memory management with Newton cooling
│   │   ├── embedding.py  # Local embedding service
│   │   ├── storage.py    # ChromaDB vector store
│   │   ├── clustering.py # Clustering suppression
│   │   ├── system.py     # Integrated memory system
│   │   └── proxy.py      # OpenAI API proxy
│   ├── models/           # Pydantic models
│   │   └── api_models.py # API request/response models
│   ├── utils/            # Utility functions
│   └── config.py         # Configuration management
├── examples/             # Example scripts
│   ├── test_api.py       # API usage examples
│   └── memory_decay_demo.py  # Visualization demo
├── main.py              # Server entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔬 Technical Details

### Memory Temperature Calculation

Each memory item tracks:
- `temperature`: Current strength (0.0 to 1.0)
- `created_at`: Creation timestamp
- `last_accessed`: Last access timestamp
- `access_count`: Number of times accessed

Temperature is recalculated on each query using:
```python
time_elapsed = current_time - last_accessed
temperature = ambient_temp + (temperature - ambient_temp) * exp(-decay_rate * time_elapsed)
```

### Clustering Suppression

When adding a new memory:
1. Calculate embedding vector
2. Find similar existing memories (cosine similarity > 0.85)
3. If similar memory exists:
   - Boost its temperature instead of creating a duplicate
   - Record reinforcement in metadata
4. Otherwise, create new memory

### User Isolation

- Each user has a separate ChromaDB collection
- Memory queries are automatically filtered by user_id
- No cross-user data leakage

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Inspired by the Ebbinghaus forgetting curve and biological memory systems
- Built with FastAPI, ChromaDB, and Transformers
- Uses Newton's Law of Cooling as a mathematical model for memory decay

## 📊 Example Output

When running the memory decay demo:

```
🧠 BionicMemory: Newton Cooling Formula Demonstration

📊 Simulation saved to /tmp/memory_decay_simulation.png

📈 Memory Decay Analysis:

Natural Decay:
  - Time to reach threshold (0.01): ~92 time units
  - Temperature after 50 time units: 0.0821

With Reinforcement:
  - Temperature after 50 time units: 0.7408
  - Temperature at end: 0.6703
  - Memory remains 'hot' (>0.01) throughout the period!
```

---

Made with ❤️ for better AI memory management
