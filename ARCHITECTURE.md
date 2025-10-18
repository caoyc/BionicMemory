# Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         BionicMemory System                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         API Layer (FastAPI)                      │
├─────────────────────────────────────────────────────────────────┤
│  • /v1/chat/completions    - OpenAI-compatible chat             │
│  • /v1/memories            - Add memories                        │
│  • /v1/memories/query      - Search memories                     │
│  • /v1/memories/stats      - Get statistics                      │
│  • /v1/memories/cleanup    - Remove cold memories                │
└─────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────┐
│                    BionicMemorySystem (Core)                     │
├─────────────────────────────────────────────────────────────────┤
│  Coordinates all components and implements business logic        │
└─────────────────────────────────────────────────────────────────┘
                    ↓              ↓              ↓
        ┌───────────────┐  ┌──────────────┐  ┌─────────────┐
        │ MemoryManager │  │EmbeddingService│  │ VectorStore │
        │               │  │                │  │  (ChromaDB) │
        │ Newton Cooling│  │  Local Model   │  │             │
        │ Temperature   │  │  Qwen/ST       │  │ Similarity  │
        │ Decay/Boost   │  │                │  │   Search    │
        └───────────────┘  └────────────────┘  └─────────────┘
                ↓
        ┌───────────────┐
        │  Clustering   │
        │  Suppressor   │
        │               │
        │ Deduplication │
        │  & Merging    │
        └───────────────┘
                ↓
        ┌───────────────┐
        │  OpenAI Proxy │
        │               │
        │ Context Inject│
        │ Memory Enhance│
        └───────────────┘
```

## Component Details

### 1. API Layer (`bionicmemory/api/app.py`)

FastAPI application providing RESTful endpoints:
- **OpenAI-compatible interface** for seamless integration
- **Memory management endpoints** for direct memory operations
- **Automatic context injection** into chat completions

### 2. BionicMemorySystem (`bionicmemory/core/system.py`)

Central orchestrator that:
- Coordinates all components
- Implements clustering suppression logic
- Manages memory lifecycle
- Handles user isolation

### 3. MemoryManager (`bionicmemory/core/memory.py`)

Core memory management with:
- **MemoryItem**: Individual memory with temperature tracking
- **Newton Cooling Formula**: T(t) = T₀ × e^(-kt)
- **Temperature-based lifecycle**: hot → warm → cold → forgotten
- **Access boosting**: Use it or lose it strategy

### 4. EmbeddingService (`bionicmemory/core/embedding.py`)

Local text embedding generation:
- Primary: Qwen2-0.5B-Instruct
- Fallback: sentence-transformers/all-MiniLM-L6-v2
- Converts text to vector representations
- Supports both CPU and GPU

### 5. VectorStore (`bionicmemory/core/storage.py`)

ChromaDB integration for:
- Vector similarity search
- Persistent storage
- User-specific collections
- Efficient retrieval

### 6. ClusteringSuppressor (`bionicmemory/core/clustering.py`)

Intelligent deduplication:
- Cosine similarity detection
- Merge similar memories
- Boost existing instead of duplicate
- Configurable threshold (default: 0.85)

### 7. OpenAIProxy (`bionicmemory/core/proxy.py`)

API proxy that:
- Forwards requests to OpenAI
- Injects relevant memories as context
- Formats memory with temperature indicators
- Transparent to end users

## Data Flow

### Adding a Memory

```
1. User → POST /v1/memories
2. API → BionicMemorySystem.add_memory()
3. Generate embedding (EmbeddingService)
4. Check for similar memories (ClusteringSuppressor)
5. If similar:
   - Boost existing memory temperature
   - Return "merged" status
6. If new:
   - Create MemoryItem (temperature=1.0)
   - Store in MemoryManager
   - Store in VectorStore
   - Return "added" status
```

### Querying Memories

```
1. User → POST /v1/memories/query
2. API → BionicMemorySystem.query_memories()
3. Update all temperatures (Newton cooling)
4. Generate query embedding (EmbeddingService)
5. Vector search (VectorStore)
6. Filter cold memories (temperature < threshold)
7. Boost accessed memories
8. Sort by temperature (hottest first)
9. Return top N results
```

### Chat with Memory

```
1. User → POST /v1/chat/completions
2. Extract user_id and last message
3. Query relevant memories
4. Format memories as context
5. Inject context before user message
6. Forward to OpenAI (OpenAIProxy)
7. Store conversation in memory
8. Return OpenAI response
```

## Memory Temperature Decay

### Newton's Law of Cooling

The core of BionicMemory is the application of Newton's cooling formula:

```
T(t) = T_ambient + (T_initial - T_ambient) × e^(-k×t)

Where:
- T(t): temperature at time t
- T_ambient: 0 (complete forgetting)
- T_initial: current temperature
- k: decay rate (configurable, default: 0.1)
- t: time elapsed since last access
```

### Temperature States

| Temperature | State | Icon | Behavior |
|------------|-------|------|----------|
| 1.0        | Fresh | 🔥   | Just created/accessed |
| 0.7 - 1.0  | Hot   | 🔥   | Active, frequently used |
| 0.3 - 0.7  | Warm  | 🌡️   | Still relevant, occasionally used |
| 0.01 - 0.3 | Cold  | ❄️   | Rarely used, cooling down |
| < 0.01     | Forgotten | ❌ | Automatically removed |

### Access Boost

When a memory is accessed:
```python
new_temperature = min(1.0, current_temperature + boost)
```

Default boost: 0.3 (configurable)

## User Isolation

Each user has:
- Separate ChromaDB collection
- Isolated memory manager entries
- No cross-user data access
- Complete privacy

Collection naming: `user_{user_id}`

## Clustering Suppression Algorithm

```python
1. Calculate embedding for new memory
2. Find existing memories with similarity > threshold
3. If similar memory found:
   a. Calculate boost = base_boost × similarity
   b. Increase existing memory temperature
   c. Update metadata (reinforcement_count++)
   d. Return merged status
4. Else:
   a. Create new memory
   b. Return added status
```

Benefits:
- Prevents duplicate memories
- Reinforces important concepts
- Maintains memory quality
- Reduces storage overhead

## Configuration

All configurable via `.env`:

```bash
# Memory decay rate (0.0 - 1.0)
# Higher = faster forgetting
MEMORY_DECAY_RATE=0.1

# Forgetting threshold (0.0 - 1.0)
# Below this, memory is deleted
MEMORY_THRESHOLD=0.01

# Similarity threshold for clustering
# Above this, memories are merged
SIMILARITY_THRESHOLD=0.85

# Memory size limits
SHORT_TERM_MEMORY_SIZE=100
LONG_TERM_MEMORY_SIZE=1000
```

## Performance Considerations

### Memory Updates

Temperature calculations are lazy:
- Calculated only when queried
- Not continuously updated
- O(1) per memory

### Vector Search

ChromaDB provides:
- Fast similarity search
- Indexed collections
- Approximate nearest neighbors
- O(log n) query time

### Storage

- In-memory: MemoryManager (fast access)
- Persistent: ChromaDB (survives restarts)
- Hybrid approach for best performance

## Scalability

Current implementation:
- Single-server deployment
- In-memory + persistent storage
- Suitable for 1-1000 users
- 1K-100K memories per user

For larger scale:
- Use Redis for memory manager
- Separate embedding service
- Distributed ChromaDB
- Load balancer for API

## Security

✅ CodeQL verified - no vulnerabilities
✅ User isolation - no data leakage
✅ No SQL injection (using ChromaDB)
✅ No sensitive data in logs
✅ Environment variables for secrets

## Future Enhancements

Potential improvements:
- [ ] Multi-model embedding support
- [ ] Distributed storage backend
- [ ] Memory importance scoring
- [ ] Automatic memory summarization
- [ ] Hierarchical memory structure
- [ ] Memory visualization dashboard
- [ ] A/B testing different decay rates
- [ ] Memory compression for old data
